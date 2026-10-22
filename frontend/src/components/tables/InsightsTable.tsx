import React, { useEffect, useState } from 'react';
import type { Insight, PaginatedResponse } from '../../types/api';
import { getInsights } from '../../services/api';
import { EmptyState, LoadingState, ErrorState } from '../common/States';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface InsightsTableProps {
  data?: PaginatedResponse<Insight> | null;
  loading?: boolean;
  page?: number;
  pageSize?: number;
  setPage?: (page: number) => void;
}

const InsightsTable: React.FC<InsightsTableProps> = ({ 
  data: externalData, 
  loading: externalLoading, 
  page: externalPage, 
  pageSize: externalPageSize = 5, 
  setPage: externalSetPage 
}) => {
  const [internalData, setInternalData] = useState<PaginatedResponse<Insight> | null>(null);
  const [internalLoading, setInternalLoading] = useState(true);
  const [internalError, setInternalError] = useState(false);
  const [internalPage, setInternalPage] = useState(1);

  const isControlled = externalData !== undefined;
  
  const data = isControlled ? externalData : internalData;
  const loading = isControlled ? (externalLoading ?? false) : internalLoading;
  const page = isControlled ? (externalPage ?? 1) : internalPage;
  const pageSize = isControlled ? externalPageSize : 5;
  
  const handleSetPage = (newPage: number) => {
    if (isControlled && externalSetPage) {
      externalSetPage(newPage);
    } else {
      setInternalPage(newPage);
    }
  };

  useEffect(() => {
    if (!isControlled) {
      const fetchData = async () => {
        setInternalLoading(true);
        setInternalError(false);
        try {
          const res = await getInsights({ page: internalPage, page_size: pageSize });
          setInternalData(res);
        } catch (e) {
          setInternalError(true);
        } finally {
          setInternalLoading(false);
        }
      };
      fetchData();
    }
  }, [internalPage, isControlled, pageSize]);

  if (loading && !data) return <LoadingState />;
  if (!isControlled && internalError && !data) return <ErrorState />;
  if (!data || data.items.length === 0) return <EmptyState message="Try adjusting your filters." />;

  const totalPages = Math.ceil(data.total / pageSize);

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      <div className="px-6 py-5 border-b border-slate-200">
        <h3 className="text-base font-semibold text-slate-800">Insights & Recommendations</h3>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <th className="px-6 py-3">Entity</th>
              <th className="px-6 py-3">Rule</th>
              <th className="px-6 py-3 w-1/3">Insight</th>
              <th className="px-6 py-3 w-1/3">Recommendation</th>
              <th className="px-6 py-3 text-right">Generated At</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {data.items.map((insight) => (
              <tr key={insight.insight_id} className="hover:bg-slate-50 transition-colors">
                <td className="px-6 py-4 align-top">
                  <div className="text-sm font-medium text-slate-900">{insight.entity_name}</div>
                  <div className="text-xs text-slate-500">{insight.entity_type} • {insight.entity_id}</div>
                </td>
                <td className="px-6 py-4 align-top text-sm">
                  <span className="px-2 py-1 text-xs font-medium bg-slate-100 text-slate-600 rounded-md whitespace-nowrap">
                    {insight.rule_name || insight.insight_type}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-slate-700 align-top">
                  <div className="break-words">
                    {insight.insight || '—'}
                  </div>
                  {insight.threshold_used && (
                    <div className="text-xs text-slate-400 mt-1 font-mono">
                      {insight.threshold_used}
                    </div>
                  )}
                </td>
                <td className="px-6 py-4 text-sm text-slate-700 align-top">
                  <div className="break-words">
                    {insight.recommendation || '—'}
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-slate-500 align-top text-right whitespace-nowrap">
                  {insight.generated_at ? new Date(insight.generated_at).toLocaleString() : '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="px-6 py-4 border-t border-slate-200 flex items-center justify-between bg-slate-50">
        <span className="text-sm text-slate-500">
          Showing <span className="font-medium text-slate-700">{data.total > 0 ? (page - 1) * pageSize + 1 : 0}</span> to <span className="font-medium text-slate-700">{Math.min(page * pageSize, data.total)}</span> of <span className="font-medium text-slate-700">{data.total}</span> entries
        </span>
        <div className="flex items-center gap-2">
          <button 
            onClick={() => handleSetPage(Math.max(1, page - 1))}
            disabled={page === 1}
            className="p-1 rounded-md border border-slate-200 bg-white text-slate-500 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 transition-colors"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <button 
            onClick={() => handleSetPage(Math.min(totalPages, page + 1))}
            disabled={page === totalPages || totalPages === 0}
            className="p-1 rounded-md border border-slate-200 bg-white text-slate-500 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-slate-50 transition-colors"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default InsightsTable;
