import React from 'react';
import { Mail, Clock, ShieldCheck } from 'lucide-react';

const Reports: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">HOD Reports Center</h1>
        <p className="mt-1 text-sm text-slate-500">
          Information regarding the automated academic intelligence report delivery system.
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-8 flex flex-col items-center text-center border-b border-slate-100 bg-slate-50/50">
          <div className="w-16 h-16 bg-brand-100 text-brand-600 rounded-full flex items-center justify-center mb-6">
            <Mail className="w-8 h-8" />
          </div>
          <h2 className="text-xl font-semibold text-slate-800 mb-2">Reports are Delivered via Email</h2>
          <p className="text-slate-600 max-w-lg mb-6">
            The Academic Intelligence Platform automatically generates comprehensive PDF and Excel reports for all departments. 
            To maintain strict data security and compliance, these reports are delivered directly to the registered email address of each Head of Department (HOD).
          </p>
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-50 text-emerald-700 rounded-lg text-sm font-medium border border-emerald-100">
            <ShieldCheck className="w-4 h-4" />
            Secure Automated Delivery Active
          </div>
        </div>

        <div className="p-8">
          <h3 className="text-sm font-semibold text-slate-800 uppercase tracking-wider mb-6">Delivery Schedule & Details</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex flex-col">
              <div className="flex items-center gap-2 text-slate-700 mb-2 font-medium">
                <Clock className="w-5 h-5 text-brand-500" />
                Schedule
              </div>
              <p className="text-sm text-slate-600">
                Reports are compiled and distributed at the end of each academic week (Sunday evening).
              </p>
            </div>
            
            <div className="flex flex-col">
              <div className="flex items-center gap-2 text-slate-700 mb-2 font-medium">
                <svg className="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                PDF Summary
              </div>
              <p className="text-sm text-slate-600">
                Contains executive summaries, key risk indicators, and performance trends for quick review.
              </p>
            </div>
            
            <div className="flex flex-col">
              <div className="flex items-center gap-2 text-slate-700 mb-2 font-medium">
                <svg className="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                Excel Data
              </div>
              <p className="text-sm text-slate-600">
                Includes granular row-level data for all students, courses, and feedback across the department.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;
