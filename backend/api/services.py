from rest_framework.response import Response
from .prompts import ANALYSIS_PROMPT, COMPARISON_PROMPT
import logging

logger = logging.getLogger(__name__)

def handle_analysis(location_name, df, model):
    try:
        matched_df = df[df['final location'] == location_name]

        if matched_df.empty:
            return Response({"error": f"No data found for location: {location_name}"}, status=404)

        # Fill NaN values with 0 before serializing
        matched_df = matched_df.fillna(0)

        chart_data = {
            "years": matched_df["year"].tolist(),
            "price": matched_df["flat - weighted average rate"].tolist(),
            "demand": matched_df["total units"].tolist(),
        }
        table_data = matched_df.to_dict(orient="records")

        data_prompt = f"""
        Here is the data for the area: {location_name}    
        Analyze the following data, focusing on residential flats.
        
        Years: {chart_data["years"]} 
        Prices (this is the 'flat - weighted average rate'): {chart_data["price"]} 
        Demand (this is the 'total units' sold): {chart_data["demand"]} 

        Raw Table Data (for additional context):
        {table_data}
        """
        
        full_prompt = f"{ANALYSIS_PROMPT}\n\n{data_prompt}"

        response = model.generate_content(full_prompt)
        ai_summary = response.text

        return Response({
            "query_type": "analysis",
            "summary": ai_summary,
            "chart": chart_data,
            "table": table_data,
            "location": location_name
        })
    except Exception as e:
        logger.error(f"An error occurred in handle_analysis for {location_name}: {e}")
        return Response({"error": f"AI generation failed for {location_name}."}, status=500)

def handle_comparison(locations, df, model):
    try:
        chart_data = []
        table_data = []
        data_prompts = []

        for location in locations:
            matched_df = df[df['final location'] == location]
            if matched_df.empty:
                continue

            # Fill NaN values with 0 before serializing
            matched_df = matched_df.fillna(0)

            chart_data.append({
                "location": location,
                "years": matched_df["year"].tolist(),
                "price": matched_df["flat - weighted average rate"].tolist(),
                "demand": matched_df["total units"].tolist(),
            })
            
            table_data.extend(matched_df.to_dict(orient="records"))

            data_prompts.append(
                "        ---\n"
                "        Data for: {location}\n"
                "        Years: {years}\n"
                "        Prices: {prices}\n"
                "        Demand: {demand}\n"
                "        Raw Table: {table}\n"
                "        ---\n".format(
                    location=location,
                    years=matched_df["year"].tolist(),
                    prices=matched_df["flat - weighted average rate"].tolist(),
                    demand=matched_df["total units"].tolist(),
                    table=matched_df.to_dict(orient="records")
                )
            )

        if not data_prompts:
            return Response({"error": "No data found for any of the locations."}, status=404)

        full_prompt = f"{COMPARISON_PROMPT}\n\nHere is the data for the locations to be compared:\n{''.join(data_prompts)}"

        response = model.generate_content(full_prompt)
        ai_summary = response.text

        return Response({
            "query_type": "comparison",
            "summary": ai_summary,
            "chart": chart_data,
            "table": table_data,
            "locations": locations
        })
    except Exception as e:
        logger.error(f"An error occurred in handle_comparison for {locations}: {e}")
        return Response({"error": "AI generation failed for comparison."}, status=500)