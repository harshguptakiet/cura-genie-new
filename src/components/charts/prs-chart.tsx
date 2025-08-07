'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2 } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  Legend
} from 'recharts';

interface PrsChartData {
  condition: string;
  score: number;
  percentile: number;
  riskLevel: 'low' | 'moderate' | 'high';
  populationAverage: number;
}

interface PrsChartProps {
  userId: string;
}

// Mock API function - replace with actual API call
const fetchPrsChartData = async (userId: string): Promise<PrsChartData[]> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1200));
  
  return [
    {
      condition: 'Type 2 Diabetes',
      score: 0.75,
      percentile: 82,
      riskLevel: 'high',
      populationAverage: 0.50
    },
    {
      condition: 'Coronary Artery Disease',
      score: 0.45,
      percentile: 35,
      riskLevel: 'low',
      populationAverage: 0.50
    },
    {
      condition: "Alzheimer's Disease",
      score: 0.62,
      percentile: 68,
      riskLevel: 'moderate',
      populationAverage: 0.50
    },
    {
      condition: 'Breast Cancer',
      score: 0.38,
      percentile: 28,
      riskLevel: 'low',
      populationAverage: 0.50
    },
    {
      condition: 'Prostate Cancer',
      score: 0.55,
      percentile: 55,
      riskLevel: 'moderate',
      populationAverage: 0.50
    },
    {
      condition: 'Rheumatoid Arthritis',
      score: 0.42,
      percentile: 32,
      riskLevel: 'low',
      populationAverage: 0.50
    }
  ];
};

const getRiskColor = (riskLevel: string) => {
  switch (riskLevel) {
    case 'high':
      return '#ef4444'; // red-500
    case 'moderate':
      return '#eab308'; // yellow-500
    case 'low':
      return '#22c55e'; // green-500
    default:
      return '#6b7280'; // gray-500
  }
};

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div className="bg-white p-4 border border-gray-200 rounded-lg shadow-lg">
        <p className="font-semibold text-gray-900">{label}</p>
        <p className="text-sm text-gray-600 mt-1">
          <span className="font-medium">Your Score:</span> {data.score.toFixed(2)}
        </p>
        <p className="text-sm text-gray-600">
          <span className="font-medium">Percentile:</span> {data.percentile}th
        </p>
        <p className="text-sm text-gray-600">
          <span className="font-medium">Population Average:</span> {data.populationAverage.toFixed(2)}
        </p>
        <p className="text-sm mt-2">
          <span className={`px-2 py-1 rounded text-xs font-medium text-white ${
            data.riskLevel === 'high' ? 'bg-red-500' :
            data.riskLevel === 'moderate' ? 'bg-yellow-500' : 'bg-green-500'
          }`}>
            {data.riskLevel.toUpperCase()} RISK
          </span>
        </p>
      </div>
    );
  }
  return null;
};

export function PrsChart({ userId }: PrsChartProps) {
  const { data: chartData, isLoading, error } = useQuery({
    queryKey: ['prs-chart', userId],
    queryFn: () => fetchPrsChartData(userId),
    enabled: !!userId,
  });

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>PRS Score Visualization</CardTitle>
          <CardDescription>Comparative view of your polygenic risk scores</CardDescription>
        </CardHeader>
        <CardContent className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin" />
          <span className="ml-2">Loading chart data...</span>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>PRS Score Visualization</CardTitle>
          <CardDescription>Comparative view of your polygenic risk scores</CardDescription>
        </CardHeader>
        <CardContent>
          <Alert variant="destructive">
            <AlertDescription>
              Failed to load chart data. Please try again later.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>PRS Score Visualization</CardTitle>
        <CardDescription>
          Your polygenic risk scores compared to population averages
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="w-full h-96">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              margin={{
                top: 20,
                right: 30,
                left: 20,
                bottom: 60,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis
                dataKey="condition"
                angle={-45}
                textAnchor="end"
                height={100}
                fontSize={12}
                interval={0}
              />
              <YAxis
                domain={[0, 1]}
                tickFormatter={(value) => value.toFixed(1)}
                fontSize={12}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              
              {/* Population Average Line */}
              <Bar
                dataKey="populationAverage"
                fill="#e5e7eb"
                name="Population Average"
                radius={[2, 2, 0, 0]}
              />
              
              {/* Your Score Bars */}
              <Bar
                dataKey="score"
                name="Your Score"
                radius={[4, 4, 0, 0]}
              >
                {chartData?.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getRiskColor(entry.riskLevel)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        <div className="mt-4 flex flex-wrap gap-4 justify-center text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-red-500 rounded"></div>
            <span>High Risk</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-yellow-500 rounded"></div>
            <span>Moderate Risk</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-green-500 rounded"></div>
            <span>Low Risk</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-gray-300 rounded"></div>
            <span>Population Average</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
