# This handles the API requests for analyzing and comparing real estate areas. It uses Google Gemini model for AI processing,( location extraction, and delegates analysis/comparison tasks.)
# we can also scale this app for agentic ai use-cases in future.

import re
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
import google.generativeai as genai
import logging
from django.conf import settings

from .data_loader import load_data
from .prompts import LOCATION_EXTRACTION_PROMPT
from .services import handle_analysis, handle_comparison

# --- 0. SETUP LOGGING ---
logger = logging.getLogger(__name__)

# --- 1. SETUP ---
df = load_data()
genai.configure(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# --- 2. VIEW LOGIC ---
@api_view(['POST'])
def handle_chat(request):
    try:
        query = request.data.get("query", "").lower()
        
        # 1. Extract location names from query using AI
        try:
            extraction_prompt = f"{LOCATION_EXTRACTION_PROMPT}\n\nUser query: {query}"
            response = model.generate_content(extraction_prompt)
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
            locations_data = json.loads(cleaned_response)
            raw_locations = locations_data.get("locations", [])
        except (Exception, json.JSONDecodeError) as e:
            logger.error(f"AI location extraction failed: {e}")
            raw_locations = re.split(r'\s*vs\s*|\s*,\s*', query)

        matched_locations = []
        for loc in raw_locations:
            if not loc.strip():
                continue
            matches = df[df['final location'].str.lower().str.contains(loc.strip(), na=False)]
            if not matches.empty:
                matched_locations.append(matches.iloc[0]['final location'])

        unique_locations = sorted(list(set(matched_locations)))

        # 2. Handle different scenarios
        if not unique_locations:
            return Response({"error": "No matching areas found for the query."}, status=404)
        
        elif len(unique_locations) == 1:
            return handle_analysis(unique_locations[0], df, model)
            
        else:
            return handle_comparison(unique_locations, df, model)
    except Exception as e:
        logger.error(f"An unexpected error occurred in handle_chat: {e}")
        return Response({"error": "An internal server error occurred."}, status=500)