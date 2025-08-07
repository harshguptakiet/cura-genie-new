'use client';

import React, { useRef, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2 } from 'lucide-react';
import * as d3 from 'd3';

interface Variant {
  chromosome: string;
  position: number;
  importance: number;
  id?: string;
  ref?: string;
  alt?: string;
  quality?: number;
}

interface GenomeBrowserProps {
  userId: string;
}

// API function to fetch real genomic variants
const fetchGenomicVariants = async (userId: string): Promise<Variant[]> => {
  const response = await fetch(`http://127.0.0.1:8000/api/genomic/variants/${userId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch genomic variants');
  }
  return response.json();
};

const GenomeBrowser: React.FC<GenomeBrowserProps> = ({ userId }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  const { data: variants, isLoading, error } = useQuery({
    queryKey: ['genomic-variants', userId],
    queryFn: () => fetchGenomicVariants(userId),
    enabled: !!userId,
    retry: 1
  });

  useEffect(() => {
    if (containerRef.current && variants && variants.length > 0) {
      drawGenomeBrowser(containerRef.current, variants);
    }
  }, [variants]);

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Genome Browser</CardTitle>
          <CardDescription>Visualize genomic variants across chromosomes</CardDescription>
        </CardHeader>
        <CardContent className="flex items-center justify-center py-12">
          <Loader2 className="h-8 w-8 animate-spin" />
          <span className="ml-2">Loading genomic variants...</span>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Genome Browser</CardTitle>
          <CardDescription>Visualize genomic variants across chromosomes</CardDescription>
        </CardHeader>
        <CardContent>
          <Alert variant="destructive">
            <AlertDescription>
              No genomic data available. Upload your VCF file to visualize variants.
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    );
  }

  if (!variants || variants.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Genome Browser</CardTitle>
          <CardDescription>Visualize genomic variants across chromosomes</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12 text-gray-500">
            <p>No genomic variants found.</p>
            <p className="text-sm mt-2">Upload your genomic data to see visualization.</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Genome Browser</CardTitle>
        <CardDescription>Visualize genomic variants across chromosomes ({variants.length} variants)</CardDescription>
      </CardHeader>
      <CardContent>
        <div ref={containerRef} className="w-full h-96"></div>
      </CardContent>
    </Card>
  );
};

function drawGenomeBrowser(container: HTMLDivElement, variants: Variant[]) {
  // Define dimensions
  const width = container.clientWidth;
  const height = container.clientHeight;
  const margins = { top: 20, right: 20, bottom: 30, left: 40 };

  // Clear previous content
  d3.select(container).select('svg').remove();

  // Create SVG container
  const svg = d3.select(container)
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  // Create a scale for the x-axis
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(variants, d => d.position) || 1])
    .range([margins.left, width - margins.right]);

  // Y-scale for chromosomes
  const chromosomes = Array.from(new Set(variants.map(v => v.chromosome)));
  const yScale = d3.scalePoint()
    .domain(chromosomes)
    .range([margins.top, height - margins.bottom]);

  // Color scale for importance
  const cScale = d3.scaleSequential(d3.interpolateReds)
    .domain([0, 1]);

  // X-axis
  svg.append('g')
    .attr('transform', `translate(0, ${height - margins.bottom})`)
    .call(d3.axisBottom(xScale))
    .selectAll('text')
    .style('font-size', '12px');

  // Y-axis
  svg.append('g')
    .attr('transform', `translate(${margins.left}, 0)`)
    .call(d3.axisLeft(yScale as any))
    .selectAll('text')
    .style('font-size', '12px');

  // Draw variants
  svg.selectAll('circle')
    .data(variants)
    .enter()
    .append('circle')
    .attr('cx', d => xScale(d.position))
    .attr('cy', d => yScale(d.chromosome) ?? 0)
    .attr('r', d => Math.sqrt(d.importance) * 8)
    .attr('fill', d => cScale(d.importance));
}

export default GenomeBrowser;

