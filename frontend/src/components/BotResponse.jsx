import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const BotResponse = ({ message }) => {
    const { summary, chart, table, query_type, location, locations } = message;

    const renderChart = () => {
        if (query_type === 'analysis') {
            const data = chart.years.map((year, index) => ({
                year,
                price: chart.price[index],
                demand: chart.demand[index],
            }));
            return (
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="year" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="price" stroke="#8884d8" name={`Price in ${location}`} />
                        <Line type="monotone" dataKey="demand" stroke="#82ca9d" name={`Demand in ${location}`} />
                    </LineChart>
                </ResponsiveContainer>
            );
        }

        if (query_type === 'comparison') {
            const colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300'];
            const allYears = [...new Set(chart.flatMap(c => c.years))].sort();
            const data = allYears.map(year => {
                const entry = { year };
                chart.forEach(c => {
                    const index = c.years.indexOf(year);
                    if (index !== -1) {
                        entry[`price_${c.location}`] = c.price[index];
                        entry[`demand_${c.location}`] = c.demand[index];
                    }
                });
                return entry;
            });

            return (
                <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="year" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        {chart.map((c, i) => (
                            <Line key={c.location} type="monotone" dataKey={`price_${c.location}`} stroke={colors[i % colors.length]} name={`Price in ${c.location}`} />
                        ))}
                        {chart.map((c, i) => (
                            <Line key={`demand_${c.location}`} type="monotone" dataKey={`demand_${c.location}`} stroke={colors[i % colors.length]} strokeDasharray="5 5" name={`Demand in ${c.location}`} />
                        ))}
                    </LineChart>
                </ResponsiveContainer>
            );
        }

        return null;
    };

    const renderTable = () => {
        if (!table || table.length === 0) return null;
        const headers = Object.keys(table[0]);
        return (
            <div className="overflow-x-auto">
                <table className="min-w-full bg-white border border-gray-200">
                    <thead>
                        <tr>
                            {headers.map(header => <th key={header} className="py-2 px-4 border-b">{header}</th>)}
                        </tr>
                    </thead>
                    <tbody>
                        {table.map((row, index) => (
                            <tr key={index}>
                                {headers.map(header => <td key={header} className="py-2 px-4 border-b text-center">{row[header]}</td>)}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    };

    return (
        <div className="p-4 bg-gray-100 rounded-lg">
            <p className="text-lg font-semibold mb-2">AI Analysis:</p>
            <div className="prose max-w-none mb-4" dangerouslySetInnerHTML={{ __html: summary.replace(/\n/g, '<br />') }} />
            <div className="my-4">
                {renderChart()}
            </div>
            <div className="my-4">
                {renderTable()}
            </div>
        </div>
    );
};

export default BotResponse;
