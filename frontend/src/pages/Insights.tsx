import React, { useEffect, useState, useMemo, useCallback } from 'react';
import { getInsights, getInsightsDistribution } from '../services/api';
import type { Insight, InsightDistributionItem, PaginatedResponse } from '../types/api';
import KpiCard from '../components/common/KpiCard';
import InsightsTable from '../components/tables/InsightsTable';
import { InsightDistributionChart } from '../components/charts/InsightDistributionChart';
import { Lightbulb, Filter, Search, RotateCcw } from 'lucide-react';
import { ErrorState } from '../components/common/States';

const Insights: React.FC = () => {
  const [distributionData, setDistributionData] = useState<InsightDistributionItem[]>([]);
  const [insightsData, setInsightsData] = useState<PaginatedResponse<Insight> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [insightType, setInsightType] = useState<string>('All');
  const [entityType, setEntityType] = useState<string>('All');
  const [search, setSearch] = useState<string>('');
  const [debouncedSearch, setDebouncedSearch] = useState<string>('');

  // Debounce search
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(search);
      setPage(1); // Reset page on search
    }, 500);
    return () => clearTimeout(handler);
  }, [search]);

  const fetchDistribution = async () => {
    try {
      const res = await getInsightsDistribution();
      setDistributionData(res);
    } catch (e) {
      console.error('Failed to fetch distribution', e);
    }
  };

  const fetchInsights = useCallback(async () => {
    setLoading(true);
    setError(false);
    try {
      const params: any = { page, page_size: pageSize };
      if (insightType !== 'All') params.insight_type = insightType;
      if (entityType !== 'All') params.entity_type = entityType;
      if (debouncedSearch) params.search = debouncedSearch;

      const res = await getInsights(params);
      setInsightsData(res);
    } catch (err) {
      setError(true);
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, insightType, entityType, debouncedSearch]);

  useEffect(() => {
    fetchDistribution();
  }, []);

  useEffect(() => {
    fetchInsights();
  }, [fetchInsights]);

  // Derive unique filters from distribution data (dynamic)
  const uniqueInsightTypes = useMemo(() => {
    const types = new Set(distributionData.map(d => d.insight_type));
    return ['All', ...Array.from(types)];
  }, [distributionData]);

  const uniqueEntityTypes = useMemo(() => {
    const types = new Set(distributionData.map(d => d.entity_type));
    return ['All', ...Array.from(types)];
  }, [distributionData]);

  // Aggregate total insights for KPI
  const totalInsights = useMemo(() => {
    return distributionData.reduce((sum, item) => sum + item.count, 0);
  }, [distributionData]);

  const handleReset = () => {
    setInsightType('All');
    setEntityType('All');
    setSearch('');
    setDebouncedSearch('');
    setPage(1);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Insights & Recommendations</h1>
        <p className="mt-1 text-sm text-slate-500">
          Deterministic insights generated from the academic analytics pipeline.
        </p>
      </div>

      {/* KPI Section */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <KpiCard
          title="Total Insights"
          value={totalInsights.toLocaleString()}
          icon={Lightbulb}
          trend={{ value: 0, isPositive: true }}
        />
        {/* We do not fabricate other KPIs here per instructions */}
      </div>

      {/* Main Content Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Left Column: Filters & Distribution */}
        <div className="lg:col-span-1 space-y-6">
          
          {/* Filters Card */}
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
            <div className="flex items-center gap-2 mb-4">
              <Filter className="w-4 h-4 text-slate-500" />
              <h2 className="text-sm font-semibold text-slate-800">Filters</h2>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-500 mb-1">Search</label>
                <div className="relative">
                  <input
                    type="text"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    placeholder="Search insights..."
                    className="w-full pl-8 pr-3 py-2 text-sm border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-500"
                  />
                  <Search className="w-4 h-4 text-slate-400 absolute left-2.5 top-2.5" />
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-500 mb-1">Insight Type</label>
                <select
                  value={insightType}
                  onChange={(e) => {
                    setInsightType(e.target.value);
                    setPage(1);
                  }}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-500"
                >
                  {uniqueInsightTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-500 mb-1">Entity Type</label>
                <select
                  value={entityType}
                  onChange={(e) => {
                    setEntityType(e.target.value);
                    setPage(1);
                  }}
                  className="w-full px-3 py-2 text-sm border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-500"
                >
                  {uniqueEntityTypes.map(type => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>

              <button
                onClick={handleReset}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 mt-2 text-sm font-medium text-slate-600 bg-slate-50 hover:bg-slate-100 rounded-md transition-colors border border-slate-200"
              >
                <RotateCcw className="w-4 h-4" />
                Reset Filters
              </button>
            </div>
          </div>

          {/* Distribution Chart Card */}
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
            <h2 className="text-sm font-semibold text-slate-800 mb-4">Insight Distribution</h2>
            <InsightDistributionChart data={distributionData} />
          </div>

        </div>

        {/* Right Column: Table */}
        <div className="lg:col-span-3">
          {error && !insightsData ? (
            <ErrorState onRetry={fetchInsights} />
          ) : (
            <InsightsTable 
              data={insightsData}
              loading={loading}
              page={page}
              pageSize={pageSize}
              setPage={setPage}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default Insights;
