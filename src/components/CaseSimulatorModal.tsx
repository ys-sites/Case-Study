import React, { useState } from 'react';
import {
  X,
  Play,
  Download,
  CheckCircle2,
  Cpu,
  Layers,
  TrendingUp,
  ShieldAlert,
  FileText,
  Presentation as PresentationIcon,
  Video,
  Award,
  ChevronRight,
  Calculator,
  Workflow,
  BookOpen,
  ArrowRight,
  Film,
} from 'lucide-react';
import solutionData from '../data/current_case_solution.json';
import sampleCases from '../data/case_index.json';
import concordiaVideos from '../data/concordia_video_registry.json';

interface CaseSimulatorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLoadCaseIntoEditor?: (markdown: string) => void;
}

export const CaseSimulatorModal: React.FC<CaseSimulatorModalProps> = ({
  isOpen,
  onClose,
  onLoadCaseIntoEditor,
}) => {
  const [activeTab, setActiveTab] = useState<'solution' | 'pinterest' | 'financials' | 'defense' | 'video' | 'agents' | 'architecture' | 'concordia'>('pinterest');
  const [concordiaCourseFilter, setConcordiaCourseFilter] = useState<string>('ALL');
  const [concordiaSearchQuery, setConcordiaSearchQuery] = useState<string>('');
  const [selectedCaseId, setSelectedCaseId] = useState(solutionData.case_identification.id);

  // Financial Interactive Simulator State
  const [targetGain, setTargetGain] = useState(24.5);
  const [unitMargin, setUnitMargin] = useState(24.5);
  const [capexBudget, setCapexBudget] = useState(1625000);

  // Calculate live financial figures
  const baselineOutput = solutionData.problem_diagnosis.baseline_value;
  const annualWorkDays = 250;
  const addedUnitsPerDay = (baselineOutput * (targetGain / 100));
  const addedAnnualRevenue = addedUnitsPerDay * annualWorkDays * (unitMargin * 2.2);
  const paybackMonths = Math.max(2.0, Number(((capexBudget / (addedAnnualRevenue * 0.45)) * 12).toFixed(1)));
  const calculatedEbitdaY3 = Math.round(addedAnnualRevenue * 0.32);

  const agents = [
    { id: 'Agent 00', name: 'Master Orchestrator', role: 'Workflow DAG & Resource Optimization', status: 'COMPLETED', badge: 'Active' },
    { id: 'Agent 01', name: 'Case Intelligence Analyst', role: 'Problem Statement & Constraint Extraction', status: 'COMPLETED', badge: 'Verified' },
    { id: 'Agent 02', name: 'Global Competition Researcher', role: '133 Historical Competition Benchmarks', status: 'COMPLETED', badge: 'Matched' },
    { id: 'Agent 03', name: 'Root Cause & Systems Analyst', role: 'Five Whys & MECE Issue Tree Modeling', status: 'COMPLETED', badge: 'Rigorous' },
    { id: 'Agent 04', name: 'Brainstorming & Innovation', role: '3 Divergent Architectural Concepts', status: 'COMPLETED', badge: 'Ranked' },
    { id: 'Agent 05', name: 'Strategy Evaluation & Decision', role: 'Multi-Criteria Weighted Matrix (9.2/10)', status: 'COMPLETED', badge: 'Selected' },
    { id: 'Agent 06', name: 'Business & Financial Modeling', role: '3-Year Proforma P&L, NPV, IRR, Payback', status: 'COMPLETED', badge: 'Accurate' },
    { id: 'Agent 07', name: 'Technical & Product Architecture', role: 'Modular Micro-Cell System Engineering', status: 'COMPLETED', badge: 'Feasible' },
    { id: 'Agent 08', name: 'Implementation Blueprint', role: '3-Horizon Roadmap & Leading/Lagging KPIs', status: 'COMPLETED', badge: 'Phased' },
    { id: 'Agent 09', name: 'Critical Reviewer / Red Team', role: '5 Adversarial Judge Defense Rebuttals', status: 'COMPLETED', badge: 'Stress-Tested' },
    { id: 'Agent 10', name: 'PDF Documentation Agent', role: 'Strategic Blueprint & Solution Executive Memo', status: 'COMPLETED', badge: '2 PDFs Ready' },
    { id: 'Agent 11', name: 'PowerPoint Presentation Agent', role: '12-Slide Master Executive Presentation Deck', status: 'COMPLETED', badge: '.pptx Ready' },
    { id: 'Agent 12', name: 'Website Development Agent', role: 'Interactive Solution Simulation & Showcase', status: 'COMPLETED', badge: 'Live UI' },
    { id: 'Agent 13', name: 'Video Production Agent', role: '120-Second Product Demonstration Video', status: 'COMPLETED', badge: 'MP4 1080p' },
    { id: 'Agent 14', name: 'QA & Integration Agent', role: 'Cross-Deliverable Verification & 7 Quality Gates', status: 'COMPLETED', badge: '100% Passed' },
  ];

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-6xl h-[90vh] flex flex-col bg-stone-50 dark:bg-stone-900 border border-stone-200 dark:border-stone-800 rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-stone-200 dark:border-stone-800 bg-white dark:bg-stone-950">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400">
              <Cpu className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-amber-500/10 text-amber-600 dark:text-amber-400">
                  {solutionData.case_identification.id}
                </span>
                <h2 className="text-lg font-bold text-stone-900 dark:text-stone-100">
                  {solutionData.case_identification.title}
                </h2>
              </div>
              <p className="text-xs text-stone-500 dark:text-stone-400">
                14-Agent Autonomous Championship Case Solution System
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                if (onLoadCaseIntoEditor) {
                  const content = `# ${solutionData.case_identification.title}\n\n## 1. Executive Summary\n${solutionData.approved_solution.value_proposition}\n\n## 2. Core Problem & Bottlenecks\n${solutionData.problem_diagnosis.core_bottleneck}\n\n## 3. Financial Metrics\n- Payback: ${solutionData.financial_summary.payback_period_months} months\n- Year 3 EBITDA: CAD $${solutionData.financial_summary.year_3_ebitda_CAD.toLocaleString()}\n`;
                  onLoadCaseIntoEditor(content);
                  onClose();
                }
              }}
              className="px-3 py-1.5 text-xs font-medium bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition flex items-center gap-1.5"
            >
              <FileText className="w-3.5 h-3.5" />
              Load into Editor
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-lg text-stone-400 hover:text-stone-600 dark:hover:text-stone-200 hover:bg-stone-100 dark:hover:bg-stone-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-stone-200 dark:border-stone-800 bg-stone-100 dark:bg-stone-900 px-6 gap-2 pt-2 overflow-x-auto">
          {[
            { id: 'pinterest', label: 'Pinterest Case Study', icon: BookOpen },
            { id: 'concordia', label: 'Concordia Motion Pipeline', icon: Film },
            { id: 'solution', label: 'Executive Summary', icon: Award },
            { id: 'financials', label: 'Financial Simulator', icon: Calculator },
            { id: 'defense', label: 'Judge Q&A Defense', icon: ShieldAlert },
            { id: 'video', label: '2-Min Video & Deck', icon: Video },
            { id: 'agents', label: '14 Agents Pipeline', icon: Layers },
            { id: 'architecture', label: 'Machine Pipeline Guide', icon: Workflow },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 px-4 py-2.5 text-xs font-semibold rounded-t-lg transition border-t-2 ${
                  isActive
                    ? 'bg-white dark:bg-stone-950 border-amber-500 text-amber-600 dark:text-amber-400'
                    : 'border-transparent text-stone-600 dark:text-stone-400 hover:text-stone-900 dark:hover:text-stone-200'
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Tab Content */}
        <div className="flex-1 overflow-y-auto p-6 bg-stone-50 dark:bg-stone-950">
          {activeTab === 'pinterest' && (
            <div className="space-y-6 max-w-5xl mx-auto font-sans">
              {/* Editorial Top Brand Header */}
              <div className="p-6 rounded-2xl bg-emerald-950 text-white border border-emerald-800 shadow-xl relative overflow-hidden">
                <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
                <div className="flex flex-wrap items-center gap-2 mb-3">
                  <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    CASE STUDY 01: DIGITAL TRANSFORMATION
                  </span>
                  <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-white/10 text-stone-200">
                    NORTHSTAR RETAIL GROUP (CAD $1.2B)
                  </span>
                  <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono text-emerald-400 bg-emerald-900/50">
                    CAPEX: CAD $13.0M / $20.0M CEILING
                  </span>
                </div>
                <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white mb-2">
                  Project ReFlow: Digital Supply Chain Transformation
                </h2>
                <p className="text-xs sm:text-sm text-stone-300 max-w-3xl leading-relaxed">
                  A deterministic turnaround blueprint for NorthStar Retail Group's 3-DC fulfillment network. 
                  By deploying Portfolio A+B (Warehouse Robotics + Intelligent Transport Optimization), NorthStar slashes 
                  late deliveries from 8.5% to 3.5%, cuts carbon emissions by 25.0%, and captures CAD $8.08M in annual net savings 
                  with +CAD $7.094M in 3-year NPV at 10% WACC while preserving CAD $7.00M in contingency cash reserves.
                </p>

                {/* Quick PDF & Model Download Links */}
                <div className="mt-5 pt-4 border-t border-emerald-800/80 flex flex-wrap gap-3">
                  <a
                    href="./cases/Project_ReFlow/Project_ReFlow_Master_Strategy_Blueprint.pdf"
                    download="Project_ReFlow_Master_Strategy_Blueprint.pdf"
                    className="px-3.5 py-2 rounded-xl text-xs font-semibold bg-emerald-500 hover:bg-emerald-400 text-stone-950 transition flex items-center gap-2 shadow-sm"
                  >
                    <Download className="w-3.5 h-3.5" />
                    Download Strategy Blueprint (PDF)
                  </a>
                  <a
                    href="./cases/Project_ReFlow/Project_ReFlow_Presentation_Deck.pdf"
                    download="Project_ReFlow_Presentation_Deck.pdf"
                    className="px-3.5 py-2 rounded-xl text-xs font-semibold bg-white/10 hover:bg-white/20 text-white border border-white/20 transition flex items-center gap-2"
                  >
                    <PresentationIcon className="w-3.5 h-3.5" />
                    Download Executive Deck (PDF)
                  </a>
                  <a
                    href="./cases/Project_ReFlow/Project_ReFlow_Financial_Model.xlsx"
                    download="Project_ReFlow_Financial_Model.xlsx"
                    className="px-3.5 py-2 rounded-xl text-xs font-semibold bg-white/10 hover:bg-white/20 text-white border border-white/20 transition flex items-center gap-2"
                  >
                    <Calculator className="w-3.5 h-3.5" />
                    Excel Financial Model (.xlsx)
                  </a>
                </div>
              </div>

              {/* 4 Pinterest Big Metric Stat Cards */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3.5">
                {[
                  {
                    value: 'CAD $13.0M',
                    label: 'CAPITAL ALLOCATION',
                    sub: 'Leaves $7.0M in Cash Reserve',
                    color: 'text-emerald-700 dark:text-emerald-400',
                    border: 'border-emerald-500/40',
                  },
                  {
                    value: 'CAD $8.08M',
                    label: 'ANNUAL NET SAVINGS',
                    sub: 'Net of OpEx and 15% Overlap',
                    color: 'text-emerald-600 dark:text-emerald-300',
                    border: 'border-emerald-500/40',
                  },
                  {
                    value: '+$7.094M',
                    label: '3-YEAR NPV @ 10%',
                    sub: 'Hurdle Cleared (137% ROI)',
                    color: 'text-emerald-700 dark:text-emerald-400',
                    border: 'border-emerald-500/40',
                  },
                  {
                    value: '19.3 Mo',
                    label: 'PAYBACK HORIZON',
                    sub: '1.61 Years Simple Payback',
                    color: 'text-amber-600 dark:text-amber-400',
                    border: 'border-amber-500/40',
                  },
                ].map((stat, i) => (
                  <div
                    key={i}
                    className={`p-4 rounded-2xl bg-white dark:bg-stone-900 border ${stat.border} shadow-sm flex flex-col justify-between`}
                  >
                    <span className="text-[10px] font-bold tracking-wider text-stone-500 dark:text-stone-400 uppercase">
                      {stat.label}
                    </span>
                    <div className={`text-2xl font-black ${stat.color} my-1`}>
                      {stat.value}
                    </div>
                    <span className="text-[11px] text-stone-600 dark:text-stone-400">
                      {stat.sub}
                    </span>
                  </div>
                ))}
              </div>

              {/* 2 Visual Circular Gauges & Operational Profile */}
              <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 shadow-sm grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
                {/* Gauge 1: Late Delivery */}
                <div className="flex flex-col items-center text-center">
                  <div className="relative w-28 h-28 flex items-center justify-center">
                    <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="40" className="text-stone-200 dark:text-stone-800 stroke-current" strokeWidth="8" fill="transparent" />
                      <circle
                        cx="50"
                        cy="50"
                        r="40"
                        className="text-emerald-600 dark:text-emerald-400 stroke-current"
                        strokeWidth="8"
                        strokeDasharray="251.2"
                        strokeDashoffset="103"
                        strokeLinecap="round"
                        fill="transparent"
                      />
                    </svg>
                    <div className="absolute flex flex-col items-center">
                      <span className="text-xl font-extrabold text-stone-900 dark:text-stone-100">3.5%</span>
                      <span className="text-[9px] uppercase font-bold text-stone-500">Target Met</span>
                    </div>
                  </div>
                  <span className="text-xs font-bold text-emerald-800 dark:text-emerald-300 mt-2">LATE DELIVERY RATE</span>
                  <span className="text-[11px] text-stone-500">Down from 8.5% baseline (Max 5.0 pt cap)</span>
                </div>

                {/* Gauge 2: Carbon Decarbonization */}
                <div className="flex flex-col items-center text-center">
                  <div className="relative w-28 h-28 flex items-center justify-center">
                    <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="40" className="text-stone-200 dark:text-stone-800 stroke-current" strokeWidth="8" fill="transparent" />
                      <circle
                        cx="50"
                        cy="50"
                        r="40"
                        className="text-emerald-500 dark:text-emerald-300 stroke-current"
                        strokeWidth="8"
                        strokeDasharray="251.2"
                        strokeDashoffset="63"
                        strokeLinecap="round"
                        fill="transparent"
                      />
                    </svg>
                    <div className="absolute flex flex-col items-center">
                      <span className="text-xl font-extrabold text-stone-900 dark:text-stone-100">-25.0%</span>
                      <span className="text-[9px] uppercase font-bold text-stone-500">Target: -20%</span>
                    </div>
                  </div>
                  <span className="text-xs font-bold text-emerald-800 dark:text-emerald-300 mt-2">LOGISTICS GHG REDUCTION</span>
                  <span className="text-[11px] text-stone-500">Saves 4,500 tonnes CO2e/yr via routing</span>
                </div>

                {/* Operational Profile */}
                <div className="border-t md:border-t-0 md:border-l border-stone-200 dark:border-stone-800 pt-4 md:pt-0 md:pl-6 space-y-2 text-xs">
                  <h4 className="font-bold text-stone-900 dark:text-stone-100 uppercase tracking-wider text-[11px]">
                    Current Network Realities
                  </h4>
                  <div className="flex justify-between py-1 border-b border-stone-100 dark:border-stone-800">
                    <span className="text-stone-500">Annual Shipped Volume:</span>
                    <span className="font-mono font-bold text-stone-800 dark:text-stone-200">12,000,000 Orders</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-stone-100 dark:border-stone-800">
                    <span className="text-stone-500">Baseline Logistics Cost:</span>
                    <span className="font-mono font-bold text-stone-800 dark:text-stone-200">$7.20 / Order ($86.4M)</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-stone-100 dark:border-stone-800">
                    <span className="text-stone-500">Trailer Cube Utilization:</span>
                    <span className="font-mono font-bold text-amber-600 dark:text-amber-400">62.0% (Sub-optimal)</span>
                  </div>
                  <div className="flex justify-between py-1">
                    <span className="text-stone-500">Fulfillment Error Rate:</span>
                    <span className="font-mono font-bold text-rose-600 dark:text-rose-400">2.4% (288,000 orders)</span>
                  </div>
                </div>
              </div>

              {/* Exhaustive 7-Portfolio Master Decision Matrix */}
              <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 shadow-sm overflow-hidden">
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <h3 className="text-sm font-bold text-stone-900 dark:text-stone-100">
                      Exhaustive 7-Portfolio Valuation Matrix (Budget &le; CAD $20.0M)
                    </h3>
                    <p className="text-[11px] text-stone-500">
                      Official 15% overlap deductions applied to secondary initiatives
                    </p>
                  </div>
                  <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
                    Winner: Portfolio A+B
                  </span>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left">
                    <thead>
                      <tr className="bg-emerald-950 text-white text-[11px] uppercase tracking-wider">
                        <th className="py-2.5 px-3 rounded-l-lg">Portfolio Candidate</th>
                        <th className="py-2.5 px-2">Capex</th>
                        <th className="py-2.5 px-2">Gross Sav</th>
                        <th className="py-2.5 px-2">Net Sav/Yr</th>
                        <th className="py-2.5 px-2">3-Yr NPV</th>
                        <th className="py-2.5 px-2">Payback</th>
                        <th className="py-2.5 px-2">Late %</th>
                        <th className="py-2.5 px-2">CO2 Cut</th>
                        <th className="py-2.5 px-3 rounded-r-lg">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-stone-100 dark:divide-stone-800">
                      {[
                        { name: 'Option A (Warehouse)', capex: '$8.0M', gross: '$6.20M', net: '$4.90M', npv: '+$4.186M', pb: '1.63 Yrs', late: '6.5%', co2: '8.0%', status: 'FAIL', isWin: false },
                        { name: 'Option B (Transport)', capex: '$5.0M', gross: '$4.80M', net: '$3.90M', npv: '+$4.699M', pb: '1.28 Yrs', late: '5.3%', co2: '18.0%', status: 'FAIL', isWin: false },
                        { name: 'Option C (Micro-Hubs)', capex: '$12.0M', gross: '$7.00M', net: '$4.80M', npv: '-$0.063M', pb: '2.50 Yrs', late: '6.0%', co2: '12.0%', status: 'FAIL', isWin: false },
                        { name: 'PORTFOLIO A + B (WINNER)', capex: '$13.0M', gross: '$10.28M', net: '$8.08M', npv: '+$7.094M', pb: '1.61 Yrs', late: '3.5%', co2: '25.0%', status: 'PASS', isWin: true },
                        { name: 'Portfolio A + C', capex: '$20.0M', gross: '$12.15M', net: '$7.84M', npv: '-$0.503M', pb: '2.55 Yrs', late: '4.0%', co2: '20.0%', status: 'FAIL', isWin: false },
                        { name: 'Portfolio B + C', capex: '$17.0M', gross: '$11.32M', net: '$8.22M', npv: '+$3.442M', pb: '2.07 Yrs', late: '3.5%', co2: '25.0%', status: 'FAIL', isWin: false },
                        { name: 'Portfolio A + B + C', capex: '$25.0M', gross: '--', net: '--', npv: '--', pb: '--', late: '--', co2: '--', status: 'EXCEED', isWin: false },
                      ].map((row, idx) => (
                        <tr
                          key={idx}
                          className={
                            row.isWin
                              ? 'bg-emerald-500/10 font-bold text-emerald-900 dark:text-emerald-200 border-y-2 border-emerald-500'
                              : 'text-stone-700 dark:text-stone-300 hover:bg-stone-50 dark:hover:bg-stone-900'
                          }
                        >
                          <td className="py-2.5 px-3 font-medium">{row.name}</td>
                          <td className="py-2.5 px-2">{row.capex}</td>
                          <td className="py-2.5 px-2">{row.gross}</td>
                          <td className="py-2.5 px-2">{row.net}</td>
                          <td className={`py-2.5 px-2 font-mono ${row.npv.includes('+') ? 'text-emerald-600 dark:text-emerald-400' : (row.npv.includes('-') ? 'text-rose-600 dark:text-rose-400' : '')}`}>
                            {row.npv}
                          </td>
                          <td className="py-2.5 px-2">{row.pb}</td>
                          <td className={`py-2.5 px-2 ${['3.5%', '4.0%'].includes(row.late) ? 'text-emerald-600 dark:text-emerald-400 font-bold' : 'text-rose-500'}`}>
                            {row.late}
                          </td>
                          <td className={`py-2.5 px-2 ${['25.0%', '20.0%'].includes(row.co2) ? 'text-emerald-600 dark:text-emerald-400 font-bold' : 'text-rose-500'}`}>
                            {row.co2}
                          </td>
                          <td className="py-2.5 px-3">
                            <span
                              className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                row.status === 'PASS'
                                  ? 'bg-emerald-500 text-white'
                                  : (row.status === 'EXCEED' ? 'bg-amber-500/20 text-amber-700 dark:text-amber-300' : 'bg-rose-500/10 text-rose-600 dark:text-rose-400')
                              }`}
                            >
                              {row.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* 3-Horizon Visual Roadmap */}
              <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 shadow-sm space-y-3">
                <h3 className="text-sm font-bold text-stone-900 dark:text-stone-100">
                  Three-Horizon Staged Implementation Roadmap
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {[
                    {
                      step: '01',
                      title: 'HORIZON 1: TRANSPORT ML',
                      timeline: 'Months 1 - 4',
                      budget: 'CAD $5.0M | VP Logistics',
                      desc: 'Deploy dynamic vehicle routing software & carrier REST/EDI APIs. Raises cube fill from 62% to 84%. Cash flow starts Month 4.',
                      color: 'border-emerald-600 text-emerald-700 dark:text-emerald-300',
                    },
                    {
                      step: '02',
                      title: 'HORIZON 2: WAREHOUSE COBOTS',
                      timeline: 'Months 3 - 6',
                      budget: 'CAD $5.5M | VP Operations',
                      desc: 'Vision-guided robotic picking AMRs in DC 1 and DC 2. Eliminates 38% picker travel drag. Full $8.08M run-rate reached at Month 6.',
                      color: 'border-emerald-500 text-emerald-600 dark:text-emerald-400',
                    },
                    {
                      step: '03',
                      title: 'HORIZON 3: DC 3 RETROFIT',
                      timeline: 'Months 7 - 12',
                      budget: 'CAD $2.5M | CTO',
                      desc: 'Extends automation into DC 3; enables dynamic cross-facility load balancing for peak seasons. Sustains 3.5% late rate permanently.',
                      color: 'border-amber-500 text-amber-600 dark:text-amber-400',
                    },
                  ].map((h, i) => (
                    <div
                      key={i}
                      className={`p-4 rounded-xl border ${h.color} bg-stone-50 dark:bg-stone-950 flex flex-col justify-between`}
                    >
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-mono font-black text-lg">{h.step}</span>
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-stone-200 dark:bg-stone-800 text-stone-700 dark:text-stone-300">
                            {h.timeline}
                          </span>
                        </div>
                        <h4 className="font-bold text-xs text-stone-900 dark:text-stone-100 mb-1">{h.title}</h4>
                        <span className="text-[10px] font-mono font-semibold text-stone-500 block mb-2">{h.budget}</span>
                        <p className="text-[11px] text-stone-600 dark:text-stone-300 leading-relaxed">{h.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* 3-Scenario Sensitivity Stress Test */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5">
                {[
                  {
                    title: 'BEAR CASE: COST OVERRUN',
                    sub: 'Capex +25% | Savings -30%',
                    metrics: [
                      { label: 'Capex Invested:', val: 'CAD $16.25M ($3.75M Buffer)' },
                      { label: 'Annual Net Savings:', val: 'CAD $5.656M / Year' },
                      { label: 'Simple Payback:', val: '2.87 Years (34.5 Months)' },
                      { label: '3-Year NPV @ 10%:', val: '+CAD $3.839M (Accretive)' },
                    ],
                    badge: 'border-amber-500 text-amber-600 dark:text-amber-400',
                  },
                  {
                    title: 'BASE PLAN: TARGET RUN-RATE',
                    sub: 'Executive Target Blueprint',
                    metrics: [
                      { label: 'Capex Invested:', val: 'CAD $13.00M ($7.00M Buffer)' },
                      { label: 'Annual Net Savings:', val: 'CAD $8.080M / Year' },
                      { label: 'Simple Payback:', val: '1.61 Years (19.3 Months)' },
                      { label: '3-Year NPV @ 10%:', val: '+CAD $7.094M (137% ROI)' },
                    ],
                    badge: 'border-emerald-600 text-emerald-700 dark:text-emerald-300 bg-emerald-500/5',
                  },
                  {
                    title: 'BULL CASE: VOLUME SURGE',
                    sub: 'Order Volume +20% (14.4M)',
                    metrics: [
                      { label: 'Capex Invested:', val: 'CAD $13.00M (Fixed Assets)' },
                      { label: 'Annual Net Savings:', val: 'CAD $9.696M / Year' },
                      { label: 'Simple Payback:', val: '1.34 Years (16.1 Months)' },
                      { label: '3-Year NPV @ 10%:', val: '+CAD $11.118M (+157%)' },
                    ],
                    badge: 'border-emerald-500 text-emerald-600 dark:text-emerald-400',
                  },
                ].map((sc, i) => (
                  <div
                    key={i}
                    className={`p-4 rounded-xl border ${sc.badge} bg-white dark:bg-stone-900 shadow-sm`}
                  >
                    <span className="text-[10px] font-bold uppercase tracking-wider block">{sc.title}</span>
                    <span className="text-[11px] text-stone-500 dark:text-stone-400 block mb-3">{sc.sub}</span>
                    <div className="space-y-1.5 text-xs">
                      {sc.metrics.map((m, idx) => (
                        <div key={idx} className="flex justify-between border-b border-stone-100 dark:border-stone-800 pb-1">
                          <span className="text-stone-500">{m.label}</span>
                          <span className="font-mono font-bold text-stone-800 dark:text-stone-200">{m.val}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              {/* Adversarial Judge Defense Cards */}
              <div className="p-5 rounded-2xl bg-white dark:bg-stone-900 border border-stone-200 dark:border-stone-800 shadow-sm space-y-3">
                <h3 className="text-sm font-bold text-stone-900 dark:text-stone-100">
                  Adversarial Red Team Judge Defense Bank
                </h3>
                <div className="space-y-2.5">
                  {[
                    {
                      q: "Why not Portfolio B+C, which offers higher gross savings ($11.32M vs $10.28M)?",
                      a: "Gross savings ignore recurring OpEx. Option C carries $2.2M in annual recurring lease and software fees, making net savings virtually equal ($8.22M for B+C vs $8.08M for A+B). However, B+C requires CAD $17.0M capex ($4.0M more). That capital drag crushes 3-year NPV to CAD $3.44M vs CAD $7.09M for A+B. Portfolio A+B generates 106% greater net economic value.",
                    },
                    {
                      q: "What if implementation costs overrun by 25% due to hardware inflation?",
                      a: "Under a 25% capex overrun, investment expands to CAD $16.25M. This remains safely below the CAD $20.0M ceiling, preserving a $3.75M liquidity cushion. Simple payback rises to 2.01 years (24.1 months), still clearing the 3-year horizon, and 3-year NPV remains strongly positive at +CAD $3.839M.",
                    },
                    {
                      q: "Why should NorthStar trust AI-driven algorithms with mission-critical fulfillment?",
                      a: "We enforce closed-loop Human-in-the-Loop governance. Automated vehicle dispatch operates on edge telematics with deterministic static fallback routes if API latency exceeds 200ms. Distribution centres can run offline for up to 72 hours, and warehouse supervisors retain manual override at all times.",
                    },
                  ].map((qa, i) => (
                    <div
                      key={i}
                      className="p-3.5 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-950 text-xs space-y-1.5"
                    >
                      <div className="flex items-start gap-2">
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 text-rose-600 dark:text-rose-400 shrink-0">
                          Judge Q0{i + 1}
                        </span>
                        <h4 className="font-semibold text-stone-900 dark:text-stone-100">
                          "{qa.q}"
                        </h4>
                      </div>
                      <p className="pl-3 border-l-2 border-emerald-500/60 text-stone-700 dark:text-stone-300 text-[11px] leading-relaxed">
                        <strong className="text-emerald-700 dark:text-emerald-400">Rebuttal: </strong>
                        {qa.a}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'concordia' && (
            <div className="space-y-6 max-w-5xl mx-auto">
              {/* Concordia Hero Banner */}
              <div className="p-6 rounded-2xl bg-[#FCFBF7] dark:bg-stone-900 border border-amber-200 dark:border-stone-800 text-stone-900 dark:text-stone-100 shadow-sm">
                <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-100 dark:bg-amber-900/40 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-700/50">
                      GINA CODY SCHOOL OF ENGINEERING
                    </span>
                    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-blue-100 dark:bg-blue-900/40 text-blue-800 dark:text-blue-300 border border-blue-300 dark:border-blue-700/50">
                      127 EDITED VIDEOS
                    </span>
                  </div>
                  <span className="text-xs font-mono text-stone-500 dark:text-stone-400">
                    Deterministic Canvas Engine · 6-Pillar Pipeline
                  </span>
                </div>
                <h3 className="text-xl font-bold tracking-tight text-stone-900 dark:text-white mb-2">
                  Concordia Engineering Illustrated Motion-Video Director
                </h3>
                <p className="text-xs text-stone-600 dark:text-stone-300 leading-relaxed max-w-3xl">
                  Comprehensive architectural standard for deterministic educational engineering films. Powered by a warm-white 
                  illustrated notebook canvas (<code className="font-mono text-amber-700 dark:text-amber-300">#FCFBF7</code>), 
                  Kokoro-82M neural narration, live KaTeX soft-mask write-on, and procedural audio mastering across four core undergraduate courses.
                </p>
                
                {/* 4 Course Counters */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 pt-4 border-t border-amber-200/60 dark:border-stone-800">
                  {[
                    { code: 'ENGR 213', label: 'Ordinary Diff. Equations', count: 28, color: 'text-blue-600 dark:text-blue-400' },
                    { code: 'MIAE 221', label: 'Materials Science & Eng.', count: 38, color: 'text-emerald-600 dark:text-emerald-400' },
                    { code: 'INDU 211', label: 'Production & Mfg Systems', count: 54, color: 'text-amber-600 dark:text-amber-400' },
                    { code: 'MIAE 215', label: 'C++ CodeLab & Memory', count: 7, color: 'text-purple-600 dark:text-purple-400' },
                  ].map((c) => (
                    <div key={c.code} className="p-3 rounded-xl bg-white/80 dark:bg-stone-950/80 border border-stone-200 dark:border-stone-800 text-center">
                      <div className={`text-lg font-bold font-mono ${c.color}`}>{c.count} Videos</div>
                      <div className="text-xs font-semibold text-stone-900 dark:text-stone-100">{c.code}</div>
                      <div className="text-[10px] text-stone-500 dark:text-stone-400 truncate">{c.label}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* The 6 Architectural Pillars Grid */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-stone-500 dark:text-stone-400 mb-3">
                  The 6 Core Architectural Pillars (Permanent Video Directive)
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5">
                  {[
                    {
                      num: '01',
                      title: 'Warm-White Notebook Style',
                      tag: 'VISUAL DIRECTION',
                      color: 'border-amber-400/80',
                      points: [
                        'Warm paper canvas (#FCFBF7) with dot grid texture',
                        'Fine dark-ink contours (#1E242B) + dimensional 3D forms',
                        'KaTeX live left-to-right 90px soft-mask write-on',
                        'Continuous motion: term updates or rotates every 3-6s',
                      ],
                    },
                    {
                      num: '02',
                      title: 'Two Video Archetypes',
                      tag: 'PEDAGOGICAL STRUCTURE',
                      color: 'border-blue-400/80',
                      points: [
                        'Archetype A (Topics): 7-stage narrative arc (Hook -> Form -> Recipe -> Examples -> Prediction -> Traps -> Recap)',
                        'Archetype B (Walkthroughs): "Solution-First" Law',
                        'Frame 0 = Step 1; never reread prompt aloud',
                        'Zero skipped algebra (every intermediate step shown)',
                      ],
                    },
                    {
                      num: '03',
                      title: 'The Patient Tutor Persona',
                      tag: 'VOICEOVER & SPEED',
                      color: 'border-emerald-400/80',
                      points: [
                        'Local Kokoro-82M neural TTS (af_heart voice)',
                        'Pacing: 0.90x to 0.96x speed (calm & conversational)',
                        'Phonetic math: "d y by d x" instead of raw LaTeX tokens',
                        '0.35s - 0.60s breathing micro-pauses after formulas',
                      ],
                    },
                    {
                      num: '04',
                      title: 'Deterministic Canvas Engine',
                      tag: 'RENDERING RUNTIME',
                      color: 'border-purple-400/80',
                      points: [
                        'Pure deterministic function of time f(t)',
                        'Headless Chromium (puppeteer-core) + FFmpeg',
                        'Scenes: write.js, xy.js, atoms.js, crystal.js, doodle.js, code.js',
                        'Generates matching warm-white high-contrast posters',
                      ],
                    },
                    {
                      num: '05',
                      title: 'Code-Synthesized Music',
                      tag: 'AUDIO & DUCKING',
                      color: 'border-rose-400/80',
                      points: [
                        'Warm ambient pad synthesized in code (< 1.5 kHz)',
                        'Sidechain ducking: 22-27 dB below speech',
                        'Procedural SFX: paper swish, pen ticks, chime',
                        'Mastered to -16 LUFS integrated loudness & -1.5 dBTP',
                      ],
                    },
                    {
                      num: '06',
                      title: 'Website Registry & Schema',
                      tag: 'INTEGRATION',
                      color: 'border-cyan-400/80',
                      points: [
                        'Synchronized in concordia/website videoSources.ts',
                        'Course-specific gates: ENGR213, MIAE221, INDU211, MIAE215',
                        'Explicit seconds-based chapter timeline markers',
                        'Strict Anonymity Law: zero personal student names',
                      ],
                    },
                  ].map((p) => (
                    <div
                      key={p.num}
                      className={`p-4 rounded-xl bg-white dark:bg-stone-950 border ${p.color} shadow-sm flex flex-col justify-between`}
                    >
                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <span className="font-mono text-xs font-bold text-stone-400 dark:text-stone-500">
                            PILLAR {p.num}
                          </span>
                          <span className="px-2 py-0.5 rounded text-[9px] font-bold bg-stone-100 dark:bg-stone-800 text-stone-700 dark:text-stone-300">
                            {p.tag}
                          </span>
                        </div>
                        <h5 className="text-sm font-bold text-stone-900 dark:text-stone-100 mb-2.5">
                          {p.title}
                        </h5>
                        <ul className="space-y-1.5 text-[11px] text-stone-600 dark:text-stone-300">
                          {p.points.map((pt, idx) => (
                            <li key={idx} className="flex items-start gap-1.5">
                              <span className="text-amber-500 font-bold mt-0.5">•</span>
                              <span>{pt}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* 127 Videos Interactive Catalog */}
              <div className="p-5 rounded-2xl bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 shadow-sm space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h4 className="text-sm font-bold text-stone-900 dark:text-stone-100">
                      Catalog of 127 Edited & Published Engineering Videos
                    </h4>
                    <p className="text-xs text-stone-500 dark:text-stone-400">
                      Filtered by course and searchable across registry IDs and lecture titles.
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <input
                      type="text"
                      placeholder="Search title, ID, or topic..."
                      value={concordiaSearchQuery}
                      onChange={(e) => setConcordiaSearchQuery(e.target.value)}
                      className="px-3 py-1.5 text-xs rounded-lg border border-stone-300 dark:border-stone-700 bg-stone-50 dark:bg-stone-900 text-stone-900 dark:text-stone-100 focus:outline-none focus:ring-1 focus:ring-amber-500 w-48 sm:w-60"
                    />
                  </div>
                </div>

                {/* Course Filter Tabs */}
                <div className="flex flex-wrap gap-2 pt-1 border-t border-stone-100 dark:border-stone-800">
                  {['ALL', 'ENGR213', 'MIAE221', 'INDU211', 'MIAE215'].map((course) => {
                    const isSelected = concordiaCourseFilter === course;
                    return (
                      <button
                        key={course}
                        onClick={() => setConcordiaCourseFilter(course)}
                        className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
                          isSelected
                            ? 'bg-amber-500 text-white shadow-sm'
                            : 'bg-stone-100 dark:bg-stone-900 text-stone-600 dark:text-stone-400 hover:bg-stone-200 dark:hover:bg-stone-800'
                        }`}
                      >
                        {course === 'ALL' ? 'All (127)' : `${course} (${concordiaVideos.filter(v => v.course === course).length})`}
                      </button>
                    );
                  })}
                </div>

                {/* Video Table List */}
                <div className="max-h-96 overflow-y-auto space-y-2 pr-1">
                  {concordiaVideos
                    .filter((v) => {
                      if (concordiaCourseFilter !== 'ALL' && v.course !== concordiaCourseFilter) return false;
                      if (!concordiaSearchQuery.trim()) return true;
                      const q = concordiaSearchQuery.toLowerCase();
                      return (
                        v.title.toLowerCase().includes(q) ||
                        v.id.toLowerCase().includes(q) ||
                        v.visual_style.toLowerCase().includes(q)
                      );
                    })
                    .slice(0, 50)
                    .map((v) => (
                      <div
                        key={v.id}
                        className="p-3 rounded-xl bg-stone-50 dark:bg-stone-900/60 border border-stone-200 dark:border-stone-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs"
                      >
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-[10px] text-stone-400 dark:text-stone-500">#{v.num}</span>
                            <span
                              className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                v.course === 'ENGR213'
                                  ? 'bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300'
                                  : v.course === 'MIAE221'
                                  ? 'bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300'
                                  : v.course === 'INDU211'
                                  ? 'bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300'
                                  : 'bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300'
                              }`}
                            >
                              {v.course}
                            </span>
                            <span className="font-semibold text-stone-900 dark:text-stone-100">{v.title}</span>
                          </div>
                          <div className="text-[11px] text-stone-500 dark:text-stone-400 font-mono truncate max-w-xl">
                            {v.id} · {v.visual_style}
                          </div>
                        </div>

                        <div className="flex items-center gap-3 text-stone-500 dark:text-stone-400 text-[11px] self-end sm:self-center font-mono">
                          <span>{v.duration_seconds}s</span>
                          <span>·</span>
                          <span>{v.chapters_count} ch</span>
                          <span className="px-1.5 py-0.5 rounded text-[9px] uppercase font-bold bg-stone-200 dark:bg-stone-800 text-stone-700 dark:text-stone-300">
                            {v.kind}
                          </span>
                        </div>
                      </div>
                    ))}
                </div>

                <div className="p-3 rounded-lg bg-stone-100 dark:bg-stone-900 text-stone-600 dark:text-stone-400 text-xs flex items-center justify-between font-mono">
                  <span>CLI Integration: python scripts/concordia_motion_director.py list</span>
                  <span className="text-amber-600 dark:text-amber-400 font-bold">127 Videos Verified</span>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'solution' && (
            <div className="space-y-6 max-w-4xl mx-auto">
              {/* Big Idea Hook */}
              <div className="p-5 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-stone-900 dark:text-stone-100">
                <span className="text-xs font-bold uppercase tracking-wider text-amber-600 dark:text-amber-400">
                  The Championship Recommendation
                </span>
                <h3 className="text-xl font-bold mt-1 mb-2 text-stone-900 dark:text-stone-100">
                  {solutionData.approved_solution.name}
                </h3>
                <p className="text-sm text-stone-700 dark:text-stone-300 leading-relaxed">
                  {solutionData.approved_solution.value_proposition}
                </p>
              </div>

              {/* Problem Diagnosis */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-stone-500 mb-2">
                    Core Bottleneck Diagnosis
                  </h4>
                  <p className="text-xs text-stone-700 dark:text-stone-300">
                    {solutionData.problem_diagnosis.core_bottleneck}
                  </p>
                  <div className="mt-4 pt-3 border-t border-stone-200 dark:border-stone-800 flex items-center justify-between text-xs">
                    <span className="text-stone-500">Baseline Throughput:</span>
                    <span className="font-mono font-bold text-stone-900 dark:text-stone-100">
                      {solutionData.problem_diagnosis.baseline_value} {solutionData.problem_diagnosis.baseline_unit}
                    </span>
                  </div>
                </div>

                <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-stone-500 mb-2">
                    Root Causes Isolated
                  </h4>
                  <ul className="space-y-1.5 text-xs text-stone-700 dark:text-stone-300">
                    {solutionData.problem_diagnosis.root_causes.map((rc, idx) => (
                      <li key={idx} className="flex items-start gap-1.5">
                        <span className="text-amber-500 font-bold">•</span>
                        <span>{rc}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Strategic Pillars */}
              <div>
                <h4 className="text-sm font-bold text-stone-900 dark:text-stone-100 mb-3">
                  Core Solution Pillars & Measured Impacts
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {solutionData.approved_solution.pillars.map((pillar, i) => (
                    <div
                      key={i}
                      className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 hover:border-amber-500/40 transition"
                    >
                      <span className="text-[11px] font-bold text-amber-600 dark:text-amber-400">
                        Pillar 0{i + 1}
                      </span>
                      <h5 className="font-semibold text-sm text-stone-900 dark:text-stone-100 mt-1 mb-2">
                        {pillar.name}
                      </h5>
                      <span className="inline-block px-2.5 py-1 text-xs font-mono font-bold rounded-md bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
                        {pillar.impact}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* 3-Horizon Roadmap */}
              <div>
                <h4 className="text-sm font-bold text-stone-900 dark:text-stone-100 mb-3">
                  Three-Horizon Implementation Roadmap
                </h4>
                <div className="space-y-2">
                  {solutionData.implementation_horizons.map((h, i) => (
                    <div
                      key={i}
                      className="p-3.5 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 flex items-center justify-between text-xs"
                    >
                      <div className="flex items-center gap-3">
                        <span className="px-2 py-1 rounded bg-stone-200 dark:bg-stone-800 font-mono font-semibold">
                          {h.horizon}
                        </span>
                        <div>
                          <span className="font-bold text-stone-900 dark:text-stone-100">{h.name}</span>
                          <span className="text-stone-500 ml-2">({h.timeline})</span>
                          <p className="text-stone-500 mt-0.5 text-[11px]">KPI: {h.kpi}</p>
                        </div>
                      </div>
                      <span className="font-mono font-bold text-amber-600 dark:text-amber-400">
                        CAD ${h.budget_CAD.toLocaleString()}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'architecture' && (
            <div className="space-y-6 max-w-4xl mx-auto">
              <div className="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
                <div className="flex items-center gap-2 mb-1">
                  <Workflow className="w-4 h-4 text-cyan-600 dark:text-cyan-400" />
                  <h3 className="font-bold text-sm text-stone-900 dark:text-stone-100">
                    How the Case Competition Machine Works: 5-Stage Architecture
                  </h3>
                </div>
                <p className="text-xs text-stone-600 dark:text-stone-300">
                  Like a high-precision industrial lathe or test rig, this system operates deterministically. 
                  Every raw case brief or dataset is processed through 5 synchronized chambers with zero skipped mathematics.
                </p>
              </div>

              {/* 5 Processing Chambers */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-stone-500">
                  The 5 Precision Chambers
                </h4>

                {[
                  {
                    chamber: 'Chamber 1',
                    title: 'Optical Intake & Decryption',
                    desc: 'PyMuPDF strips layout noise, parses tables/CSVs, extracts raw constraints, and distinguishes verified evidence from assumptions.',
                    agent: 'Agents 00 & 01',
                    color: 'border-cyan-500 text-cyan-600 dark:text-cyan-400 bg-cyan-500/5',
                  },
                  {
                    chamber: 'Chamber 2',
                    title: 'Graphify Neural Brain & Issue Trees',
                    desc: 'Traverses knowledge graph across 39 skills and 132+ global case benchmarks (Wharton, Harvard, Rotman) to isolate the core bottleneck.',
                    agent: 'Agents 02 & 03',
                    color: 'border-purple-500 text-purple-600 dark:text-purple-400 bg-purple-500/5',
                  },
                  {
                    chamber: 'Chamber 3',
                    title: 'Hydraulic Strategy Press & Decision Matrix',
                    desc: 'Generates 3-5 distinct strategic archetypes and scores each against the official competition rubric using weighted utility formulas.',
                    agent: 'Agents 04 & 05',
                    color: 'border-amber-500 text-amber-600 dark:text-amber-400 bg-amber-500/5',
                  },
                  {
                    chamber: 'Chamber 4',
                    title: 'Quantitative Financial Reactor',
                    desc: "Applies Little's Law, Theory of Constraints, and 3-year proforma statements tested under Bear (-20%), Base, and Bull (+25%) scenarios.",
                    agent: 'Agents 06, 07 & 08',
                    color: 'border-emerald-500 text-emerald-600 dark:text-emerald-400 bg-emerald-500/5',
                  },
                  {
                    chamber: 'Chamber 5',
                    title: 'Omnichannel Deliverable Conveyor',
                    desc: 'Compiles the full championship suite: 2 PDFs, 12 PPTX slides, Excel model, 112s explainer video, and this live interactive web app.',
                    agent: 'Agents 09, 10, 11 & 12',
                    color: 'border-rose-500 text-rose-600 dark:text-rose-400 bg-rose-500/5',
                  },
                ].map((c, i) => (
                  <div
                    key={c.chamber}
                    className={`p-3.5 rounded-xl border ${c.color} flex items-start justify-between gap-3`}
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-xs">{c.chamber}:</span>
                        <span className="font-semibold text-stone-900 dark:text-stone-100 text-xs">
                          {c.title}
                        </span>
                      </div>
                      <p className="text-[11px] text-stone-600 dark:text-stone-300 mt-1 leading-relaxed">
                        {c.desc}
                      </p>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-stone-200 dark:bg-stone-800 text-stone-700 dark:text-stone-300 shrink-0">
                      {c.agent}
                    </span>
                  </div>
                ))}
              </div>

              {/* Formula Sheet */}
              <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900">
                <h4 className="text-xs font-bold text-stone-900 dark:text-stone-100 mb-2">
                  Standard Industrial & Financial Formulas Applied
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-cyan-600 dark:text-cyan-400 block mb-1">
                      Little's Law (Queueing Flow)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      WIP = Throughput (TH) x Cycle Time (CT)
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-purple-600 dark:text-purple-400 block mb-1">
                      Theory of Constraints (Bottlenecks)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      Throughput_sys = min(R1, R2, ..., Rn)
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-amber-600 dark:text-amber-400 block mb-1">
                      Unit Economics (LTV / CAC)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      LTV = (ARPU x Margin %) / Churn &ge; 3.0x CAC
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 block mb-1">
                      Breakeven Volume (BEP)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      BEP = Fixed Capex / Unit Contribution Margin
                    </p>
                  </div>
                </div>
              </div>

              {/* Documentation Assets */}
              <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-900 text-white space-y-3">
                <div className="flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-cyan-400" />
                  <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-400">
                    Official System Documentation Assets
                  </h4>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  <div className="p-2.5 rounded-lg bg-stone-800/80 border border-stone-700/60">
                    <span className="font-semibold block text-stone-200">System Pipeline Guide (PDF)</span>
                    <span className="text-[10px] text-stone-400 font-mono">docs/CASE_COMPETITION_SYSTEM_PIPELINE_GUIDE.pdf</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-stone-800/80 border border-stone-700/60">
                    <span className="font-semibold block text-stone-200">How the Machine Works (Guide)</span>
                    <span className="text-[10px] text-stone-400 font-mono">docs/HOW_THE_CASE_MACHINE_WORKS.md</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'financials' && (
            <div className="space-y-6 max-w-4xl mx-auto">
              <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
                <h3 className="font-bold text-sm text-stone-900 dark:text-stone-100">
                  Interactive Sensitivity & Unit Economics Engine
                </h3>
                <p className="text-xs text-stone-600 dark:text-stone-300 mt-1">
                  Adjust implementation assumptions below to recalculate real-time EBITDA, payback horizon, and ROI.
                </p>
              </div>

              {/* Sliders */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900">
                <div>
                  <div className="flex justify-between text-xs font-semibold mb-1">
                    <span>Target Throughput Gain</span>
                    <span className="text-amber-600 font-mono">+{targetGain}%</span>
                  </div>
                  <input
                    type="range"
                    min="10"
                    max="40"
                    step="0.5"
                    value={targetGain}
                    onChange={(e) => setTargetGain(Number(e.target.value))}
                    className="w-full accent-amber-500"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-xs font-semibold mb-1">
                    <span>Unit Contribution Margin</span>
                    <span className="text-amber-600 font-mono">${unitMargin} CAD</span>
                  </div>
                  <input
                    type="range"
                    min="15"
                    max="45"
                    step="0.5"
                    value={unitMargin}
                    onChange={(e) => setUnitMargin(Number(e.target.value))}
                    className="w-full accent-amber-500"
                  />
                </div>

                <div>
                  <div className="flex justify-between text-xs font-semibold mb-1">
                    <span>CapEx Ceiling</span>
                    <span className="text-amber-600 font-mono">${(capexBudget / 1000).toFixed(0)}k</span>
                  </div>
                  <input
                    type="range"
                    min="1000000"
                    max="2500000"
                    step="25000"
                    value={capexBudget}
                    onChange={(e) => setCapexBudget(Number(e.target.value))}
                    className="w-full accent-amber-500"
                  />
                </div>
              </div>

              {/* Real-time calculated cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 text-center">
                  <span className="text-xs text-stone-500 font-semibold">Payback Period</span>
                  <div className="text-2xl font-bold font-mono text-emerald-600 dark:text-emerald-400 mt-1">
                    {paybackMonths} Mo
                  </div>
                  <span className="text-[11px] text-stone-400">Target: &lt;12.0 Months</span>
                </div>

                <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 text-center">
                  <span className="text-xs text-stone-500 font-semibold">Year 3 EBITDA</span>
                  <div className="text-2xl font-bold font-mono text-stone-900 dark:text-stone-100 mt-1">
                    ${(calculatedEbitdaY3 / 1000000).toFixed(2)}M
                  </div>
                  <span className="text-[11px] text-stone-400">32.0% Margin Hurdle</span>
                </div>

                <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 text-center">
                  <span className="text-xs text-stone-500 font-semibold">LTV / CAC Ratio</span>
                  <div className="text-2xl font-bold font-mono text-amber-600 dark:text-amber-400 mt-1">
                    {solutionData.financial_summary.ltv_to_cac_ratio}x
                  </div>
                  <span className="text-[11px] text-stone-400">Benchmark: &ge;3.0x</span>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'architecture' && (
            <div className="space-y-6 max-w-4xl mx-auto">
              <div className="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
                <div className="flex items-center gap-2 mb-1">
                  <Workflow className="w-4 h-4 text-cyan-600 dark:text-cyan-400" />
                  <h3 className="font-bold text-sm text-stone-900 dark:text-stone-100">
                    How the Case Competition Machine Works: 5-Stage Architecture
                  </h3>
                </div>
                <p className="text-xs text-stone-600 dark:text-stone-300">
                  Like a high-precision industrial lathe or test rig, this system operates deterministically. 
                  Every raw case brief or dataset is processed through 5 synchronized chambers with zero skipped mathematics.
                </p>
              </div>

              {/* 5 Processing Chambers */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-stone-500">
                  The 5 Precision Chambers
                </h4>

                {[
                  {
                    chamber: 'Chamber 1',
                    title: 'Optical Intake & Decryption',
                    desc: 'PyMuPDF strips layout noise, parses tables/CSVs, extracts raw constraints, and distinguishes verified evidence from assumptions.',
                    agent: 'Agents 00 & 01',
                    color: 'border-cyan-500 text-cyan-600 dark:text-cyan-400 bg-cyan-500/5',
                  },
                  {
                    chamber: 'Chamber 2',
                    title: 'Graphify Neural Brain & Issue Trees',
                    desc: 'Traverses knowledge graph across 39 skills and 132+ global case benchmarks (Wharton, Harvard, Rotman) to isolate the core bottleneck.',
                    agent: 'Agents 02 & 03',
                    color: 'border-purple-500 text-purple-600 dark:text-purple-400 bg-purple-500/5',
                  },
                  {
                    chamber: 'Chamber 3',
                    title: 'Hydraulic Strategy Press & Decision Matrix',
                    desc: 'Generates 3-5 distinct strategic archetypes and scores each against the official competition rubric using weighted utility formulas.',
                    agent: 'Agents 04 & 05',
                    color: 'border-amber-500 text-amber-600 dark:text-amber-400 bg-amber-500/5',
                  },
                  {
                    chamber: 'Chamber 4',
                    title: 'Quantitative Financial Reactor',
                    desc: "Applies Little's Law, Theory of Constraints, and 3-year proforma statements tested under Bear (-20%), Base, and Bull (+25%) scenarios.",
                    agent: 'Agents 06, 07 & 08',
                    color: 'border-emerald-500 text-emerald-600 dark:text-emerald-400 bg-emerald-500/5',
                  },
                  {
                    chamber: 'Chamber 5',
                    title: 'Omnichannel Deliverable Conveyor',
                    desc: 'Compiles the full championship suite: 2 PDFs, 12 PPTX slides, Excel model, 112s explainer video, and this live interactive web app.',
                    agent: 'Agents 09, 10, 11 & 12',
                    color: 'border-rose-500 text-rose-600 dark:text-rose-400 bg-rose-500/5',
                  },
                ].map((c, i) => (
                  <div
                    key={c.chamber}
                    className={`p-3.5 rounded-xl border ${c.color} flex items-start justify-between gap-3`}
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-xs">{c.chamber}:</span>
                        <span className="font-semibold text-stone-900 dark:text-stone-100 text-xs">
                          {c.title}
                        </span>
                      </div>
                      <p className="text-[11px] text-stone-600 dark:text-stone-300 mt-1 leading-relaxed">
                        {c.desc}
                      </p>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-stone-200 dark:bg-stone-800 text-stone-700 dark:text-stone-300 shrink-0">
                      {c.agent}
                    </span>
                  </div>
                ))}
              </div>

              {/* Formula Sheet */}
              <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900">
                <h4 className="text-xs font-bold text-stone-900 dark:text-stone-100 mb-2">
                  Standard Industrial & Financial Formulas Applied
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-cyan-600 dark:text-cyan-400 block mb-1">
                      Little's Law (Queueing Flow)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      WIP = Throughput (TH) x Cycle Time (CT)
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-purple-600 dark:text-purple-400 block mb-1">
                      Theory of Constraints (Bottlenecks)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      Throughput_sys = min(R1, R2, ..., Rn)
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-amber-600 dark:text-amber-400 block mb-1">
                      Unit Economics (LTV / CAC)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      LTV = (ARPU x Margin %) / Churn &ge; 3.0x CAC
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 block mb-1">
                      Breakeven Volume (BEP)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      BEP = Fixed Capex / Unit Contribution Margin
                    </p>
                  </div>
                </div>
              </div>

              {/* Documentation Assets */}
              <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-900 text-white space-y-3">
                <div className="flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-cyan-400" />
                  <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-400">
                    Official System Documentation Assets
                  </h4>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  <div className="p-2.5 rounded-lg bg-stone-800/80 border border-stone-700/60">
                    <span className="font-semibold block text-stone-200">System Pipeline Guide (PDF)</span>
                    <span className="text-[10px] text-stone-400 font-mono">docs/CASE_COMPETITION_SYSTEM_PIPELINE_GUIDE.pdf</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-stone-800/80 border border-stone-700/60">
                    <span className="font-semibold block text-stone-200">How the Machine Works (Guide)</span>
                    <span className="text-[10px] text-stone-400 font-mono">docs/HOW_THE_CASE_MACHINE_WORKS.md</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'defense' && (
            <div className="space-y-4 max-w-4xl mx-auto">
              <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 mb-4">
                <h3 className="font-bold text-sm text-stone-900 dark:text-stone-100">
                  Adversarial Red Team Judge Defense Bank
                </h3>
                <p className="text-xs text-stone-600 dark:text-stone-300 mt-1">
                  Anticipating tough executive questions from consulting partners and enterprise buyers.
                </p>
              </div>

              {solutionData.red_team_defense.map((qa, i) => (
                <div
                  key={i}
                  className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 space-y-2"
                >
                  <div className="flex items-start gap-2">
                    <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-rose-500/10 text-rose-600 dark:text-rose-400 shrink-0">
                      Judge Challenge
                    </span>
                    <h4 className="text-xs font-semibold text-stone-900 dark:text-stone-100">
                      "{qa.question}"
                    </h4>
                  </div>
                  <div className="pl-4 border-l-2 border-emerald-500/60">
                    <span className="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider block mb-1">
                      Evidence-Backed Rebuttal
                    </span>
                    <p className="text-xs text-stone-700 dark:text-stone-300 leading-relaxed">
                      {qa.rebuttal}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'video' && (
            <div className="space-y-6 max-w-4xl mx-auto">
              <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
                <h3 className="font-bold text-sm text-stone-900 dark:text-stone-100 flex items-center gap-2">
                  <Video className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                  Project ReFlow Video Production & Deliverables Suite
                </h3>
                <p className="text-xs text-stone-600 dark:text-stone-300 mt-1">
                  1080p Full HD video explainers produced with <code>001 Main/motion-video-director</code>, synchronized neural voiceovers, and procedural soundscapes.
                </p>
              </div>

              {/* Video Player Card */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-5 rounded-2xl border border-emerald-500/40 bg-stone-950 text-white flex flex-col justify-between min-h-[220px]">
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                        OFFICIAL CASE EXPLAINER (5M 15S)
                      </span>
                      <span className="text-[10px] text-stone-400 font-mono">1080p | 30 FPS</span>
                    </div>
                    <h4 className="text-sm font-bold text-white mb-1">Project ReFlow Master Solution Explainer</h4>
                    <p className="text-[11px] text-stone-400 leading-relaxed mb-3">
                      Complete 6-scene walkthrough explaining NorthStar Retail Group's baseline, MECE diagnosis, 7-portfolio matrix, 3-year DCF schedule, ESG decarbonization, and judge defense.
                    </p>
                  </div>
                  <a
                    href="./cases/Project_ReFlow/Project_ReFlow_Explainer_Video.mp4"
                    download="Project_ReFlow_Explainer_Video.mp4"
                    className="w-full py-2 px-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-stone-950 font-bold text-xs transition flex items-center justify-center gap-2 shadow-sm"
                  >
                    <Download className="w-3.5 h-3.5" />
                    Download Case Video (7.5 MB MP4)
                  </a>
                </div>

                <div className="p-5 rounded-2xl border border-stone-800 bg-stone-950 text-white flex flex-col justify-between min-h-[220px]">
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                        ARCHITECTURE GUIDE (112S)
                      </span>
                      <span className="text-[10px] text-stone-400 font-mono">1080p | 30 FPS</span>
                    </div>
                    <h4 className="text-sm font-bold text-white mb-1">System Architecture Machine Explainer</h4>
                    <p className="text-[11px] text-stone-400 leading-relaxed mb-3">
                      Overview of the 5-chamber case competition engine, Graphify knowledge traversal across 132+ benchmarks, and the 14-agent DAG pipeline.
                    </p>
                  </div>
                  <a
                    href="./Finished Resources/09_Video/System_Architecture_Explainer.mp4"
                    download="System_Architecture_Explainer.mp4"
                    className="w-full py-2 px-3 rounded-xl bg-stone-800 hover:bg-stone-700 text-white font-medium text-xs border border-stone-700 transition flex items-center justify-center gap-2"
                  >
                    <Download className="w-3.5 h-3.5" />
                    Download System Video (2.2 MB MP4)
                  </a>
                </div>
              </div>

              {/* Direct Deliverable Files */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <a
                  href="./cases/Project_ReFlow/Project_ReFlow_Master_Strategy_Blueprint.pdf"
                  download="Project_ReFlow_Master_Strategy_Blueprint.pdf"
                  className="p-3.5 rounded-xl border border-emerald-500/30 bg-emerald-500/5 hover:bg-emerald-500/10 transition flex items-center justify-between text-xs"
                >
                  <div className="flex items-center gap-2.5">
                    <FileText className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                    <div>
                      <div className="font-semibold text-stone-900 dark:text-stone-100">Project_ReFlow_Master_Strategy_Blueprint.pdf</div>
                      <div className="text-[11px] text-stone-400">cases/Project_ReFlow (4-Page Pinterest Layout)</div>
                    </div>
                  </div>
                  <span className="font-mono text-emerald-600 font-bold">PDF Ready</span>
                </a>

                <a
                  href="./cases/Project_ReFlow/Project_ReFlow_Presentation_Deck.pdf"
                  download="Project_ReFlow_Presentation_Deck.pdf"
                  className="p-3.5 rounded-xl border border-emerald-500/30 bg-emerald-500/5 hover:bg-emerald-500/10 transition flex items-center justify-between text-xs"
                >
                  <div className="flex items-center gap-2.5">
                    <PresentationIcon className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                    <div>
                      <div className="font-semibold text-stone-900 dark:text-stone-100">Project_ReFlow_Presentation_Deck.pdf</div>
                      <div className="text-[11px] text-stone-400">cases/Project_ReFlow (12 Widescreen Slides)</div>
                    </div>
                  </div>
                  <span className="font-mono text-emerald-600 font-bold">12 Slides</span>
                </a>

                <a
                  href="./cases/Project_ReFlow/Project_ReFlow_Financial_Model.xlsx"
                  download="Project_ReFlow_Financial_Model.xlsx"
                  className="p-3.5 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 hover:border-emerald-500/40 transition flex items-center justify-between text-xs"
                >
                  <div className="flex items-center gap-2.5">
                    <Calculator className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                    <div>
                      <div className="font-semibold text-stone-900 dark:text-stone-100">Project_ReFlow_Financial_Model.xlsx</div>
                      <div className="text-[11px] text-stone-400">Multi-Tab Proforma Excel Engine</div>
                    </div>
                  </div>
                  <span className="font-mono text-emerald-600 font-bold">Excel Model</span>
                </a>

                <a
                  href="./cases/Project_ReFlow/video/plan/beats.json"
                  className="p-3.5 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 hover:border-emerald-500/40 transition flex items-center justify-between text-xs"
                >
                  <div className="flex items-center gap-2.5">
                    <Workflow className="w-4 h-4 text-cyan-600 dark:text-cyan-400" />
                    <div>
                      <div className="font-semibold text-stone-900 dark:text-stone-100">beats.json (Timing Cues)</div>
                      <div className="text-[11px] text-stone-400">cases/Project_ReFlow/video/plan</div>
                    </div>
                  </div>
                  <span className="font-mono text-cyan-600 font-bold">6 Beats Synced</span>
                </a>
              </div>
            </div>
          )}

          {activeTab === 'architecture' && (
            <div className="space-y-6 max-w-4xl mx-auto">
              <div className="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
                <div className="flex items-center gap-2 mb-1">
                  <Workflow className="w-4 h-4 text-cyan-600 dark:text-cyan-400" />
                  <h3 className="font-bold text-sm text-stone-900 dark:text-stone-100">
                    How the Case Competition Machine Works: 5-Stage Architecture
                  </h3>
                </div>
                <p className="text-xs text-stone-600 dark:text-stone-300">
                  Like a high-precision industrial lathe or test rig, this system operates deterministically. 
                  Every raw case brief or dataset is processed through 5 synchronized chambers with zero skipped mathematics.
                </p>
              </div>

              {/* 5 Processing Chambers */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-stone-500">
                  The 5 Precision Chambers
                </h4>

                {[
                  {
                    chamber: 'Chamber 1',
                    title: 'Optical Intake & Decryption',
                    desc: 'PyMuPDF strips layout noise, parses tables/CSVs, extracts raw constraints, and distinguishes verified evidence from assumptions.',
                    agent: 'Agents 00 & 01',
                    color: 'border-cyan-500 text-cyan-600 dark:text-cyan-400 bg-cyan-500/5',
                  },
                  {
                    chamber: 'Chamber 2',
                    title: 'Graphify Neural Brain & Issue Trees',
                    desc: 'Traverses knowledge graph across 39 skills and 132+ global case benchmarks (Wharton, Harvard, Rotman) to isolate the core bottleneck.',
                    agent: 'Agents 02 & 03',
                    color: 'border-purple-500 text-purple-600 dark:text-purple-400 bg-purple-500/5',
                  },
                  {
                    chamber: 'Chamber 3',
                    title: 'Hydraulic Strategy Press & Decision Matrix',
                    desc: 'Generates 3-5 distinct strategic archetypes and scores each against the official competition rubric using weighted utility formulas.',
                    agent: 'Agents 04 & 05',
                    color: 'border-amber-500 text-amber-600 dark:text-amber-400 bg-amber-500/5',
                  },
                  {
                    chamber: 'Chamber 4',
                    title: 'Quantitative Financial Reactor',
                    desc: "Applies Little's Law, Theory of Constraints, and 3-year proforma statements tested under Bear (-20%), Base, and Bull (+25%) scenarios.",
                    agent: 'Agents 06, 07 & 08',
                    color: 'border-emerald-500 text-emerald-600 dark:text-emerald-400 bg-emerald-500/5',
                  },
                  {
                    chamber: 'Chamber 5',
                    title: 'Omnichannel Deliverable Conveyor',
                    desc: 'Compiles the full championship suite: 2 PDFs, 12 PPTX slides, Excel model, 112s explainer video, and this live interactive web app.',
                    agent: 'Agents 09, 10, 11 & 12',
                    color: 'border-rose-500 text-rose-600 dark:text-rose-400 bg-rose-500/5',
                  },
                ].map((c, i) => (
                  <div
                    key={c.chamber}
                    className={`p-3.5 rounded-xl border ${c.color} flex items-start justify-between gap-3`}
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-xs">{c.chamber}:</span>
                        <span className="font-semibold text-stone-900 dark:text-stone-100 text-xs">
                          {c.title}
                        </span>
                      </div>
                      <p className="text-[11px] text-stone-600 dark:text-stone-300 mt-1 leading-relaxed">
                        {c.desc}
                      </p>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-stone-200 dark:bg-stone-800 text-stone-700 dark:text-stone-300 shrink-0">
                      {c.agent}
                    </span>
                  </div>
                ))}
              </div>

              {/* Formula Sheet */}
              <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900">
                <h4 className="text-xs font-bold text-stone-900 dark:text-stone-100 mb-2">
                  Standard Industrial & Financial Formulas Applied
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-cyan-600 dark:text-cyan-400 block mb-1">
                      Little's Law (Queueing Flow)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      WIP = Throughput (TH) x Cycle Time (CT)
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-purple-600 dark:text-purple-400 block mb-1">
                      Theory of Constraints (Bottlenecks)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      Throughput_sys = min(R1, R2, ..., Rn)
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-amber-600 dark:text-amber-400 block mb-1">
                      Unit Economics (LTV / CAC)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      LTV = (ARPU x Margin %) / Churn &ge; 3.0x CAC
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 block mb-1">
                      Breakeven Volume (BEP)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      BEP = Fixed Capex / Unit Contribution Margin
                    </p>
                  </div>
                </div>
              </div>

              {/* Documentation Assets */}
              <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-900 text-white space-y-3">
                <div className="flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-cyan-400" />
                  <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-400">
                    Official System Documentation Assets
                  </h4>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  <div className="p-2.5 rounded-lg bg-stone-800/80 border border-stone-700/60">
                    <span className="font-semibold block text-stone-200">System Pipeline Guide (PDF)</span>
                    <span className="text-[10px] text-stone-400 font-mono">docs/CASE_COMPETITION_SYSTEM_PIPELINE_GUIDE.pdf</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-stone-800/80 border border-stone-700/60">
                    <span className="font-semibold block text-stone-200">How the Machine Works (Guide)</span>
                    <span className="text-[10px] text-stone-400 font-mono">docs/HOW_THE_CASE_MACHINE_WORKS.md</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'agents' && (
            <div className="space-y-4 max-w-4xl mx-auto">
              <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 mb-2">
                <h3 className="font-bold text-sm text-stone-900 dark:text-stone-100">
                  14-Agent Coordinated Intelligence Pipeline
                </h3>
                <p className="text-xs text-stone-600 dark:text-stone-300 mt-1">
                  Each agent operates under defined responsibilities, passing structured data to the canonical solution_spec.json.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {agents.map((agent) => (
                  <div
                    key={agent.id}
                    className="p-3 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 flex items-start justify-between text-xs"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-amber-600 dark:text-amber-400">
                          {agent.id}
                        </span>
                        <span className="font-semibold text-stone-900 dark:text-stone-100">
                          {agent.name}
                        </span>
                      </div>
                      <p className="text-stone-500 mt-1 text-[11px]">{agent.role}</p>
                    </div>
                    <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 shrink-0">
                      {agent.badge}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'architecture' && (
            <div className="space-y-6 max-w-4xl mx-auto">
              <div className="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
                <div className="flex items-center gap-2 mb-1">
                  <Workflow className="w-4 h-4 text-cyan-600 dark:text-cyan-400" />
                  <h3 className="font-bold text-sm text-stone-900 dark:text-stone-100">
                    How the Case Competition Machine Works: 5-Stage Architecture
                  </h3>
                </div>
                <p className="text-xs text-stone-600 dark:text-stone-300">
                  Like a high-precision industrial lathe or test rig, this system operates deterministically. 
                  Every raw case brief or dataset is processed through 5 synchronized chambers with zero skipped mathematics.
                </p>
              </div>

              {/* 5 Processing Chambers */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-stone-500">
                  The 5 Precision Chambers
                </h4>

                {[
                  {
                    chamber: 'Chamber 1',
                    title: 'Optical Intake & Decryption',
                    desc: 'PyMuPDF strips layout noise, parses tables/CSVs, extracts raw constraints, and distinguishes verified evidence from assumptions.',
                    agent: 'Agents 00 & 01',
                    color: 'border-cyan-500 text-cyan-600 dark:text-cyan-400 bg-cyan-500/5',
                  },
                  {
                    chamber: 'Chamber 2',
                    title: 'Graphify Neural Brain & Issue Trees',
                    desc: 'Traverses knowledge graph across 39 skills and 132+ global case benchmarks (Wharton, Harvard, Rotman) to isolate the core bottleneck.',
                    agent: 'Agents 02 & 03',
                    color: 'border-purple-500 text-purple-600 dark:text-purple-400 bg-purple-500/5',
                  },
                  {
                    chamber: 'Chamber 3',
                    title: 'Hydraulic Strategy Press & Decision Matrix',
                    desc: 'Generates 3-5 distinct strategic archetypes and scores each against the official competition rubric using weighted utility formulas.',
                    agent: 'Agents 04 & 05',
                    color: 'border-amber-500 text-amber-600 dark:text-amber-400 bg-amber-500/5',
                  },
                  {
                    chamber: 'Chamber 4',
                    title: 'Quantitative Financial Reactor',
                    desc: "Applies Little's Law, Theory of Constraints, and 3-year proforma statements tested under Bear (-20%), Base, and Bull (+25%) scenarios.",
                    agent: 'Agents 06, 07 & 08',
                    color: 'border-emerald-500 text-emerald-600 dark:text-emerald-400 bg-emerald-500/5',
                  },
                  {
                    chamber: 'Chamber 5',
                    title: 'Omnichannel Deliverable Conveyor',
                    desc: 'Compiles the full championship suite: 2 PDFs, 12 PPTX slides, Excel model, 112s explainer video, and this live interactive web app.',
                    agent: 'Agents 09, 10, 11 & 12',
                    color: 'border-rose-500 text-rose-600 dark:text-rose-400 bg-rose-500/5',
                  },
                ].map((c, i) => (
                  <div
                    key={c.chamber}
                    className={`p-3.5 rounded-xl border ${c.color} flex items-start justify-between gap-3`}
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-xs">{c.chamber}:</span>
                        <span className="font-semibold text-stone-900 dark:text-stone-100 text-xs">
                          {c.title}
                        </span>
                      </div>
                      <p className="text-[11px] text-stone-600 dark:text-stone-300 mt-1 leading-relaxed">
                        {c.desc}
                      </p>
                    </div>
                    <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-stone-200 dark:bg-stone-800 text-stone-700 dark:text-stone-300 shrink-0">
                      {c.agent}
                    </span>
                  </div>
                ))}
              </div>

              {/* Formula Sheet */}
              <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900">
                <h4 className="text-xs font-bold text-stone-900 dark:text-stone-100 mb-2">
                  Standard Industrial & Financial Formulas Applied
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-cyan-600 dark:text-cyan-400 block mb-1">
                      Little's Law (Queueing Flow)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      WIP = Throughput (TH) x Cycle Time (CT)
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-purple-600 dark:text-purple-400 block mb-1">
                      Theory of Constraints (Bottlenecks)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      Throughput_sys = min(R1, R2, ..., Rn)
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-amber-600 dark:text-amber-400 block mb-1">
                      Unit Economics (LTV / CAC)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      LTV = (ARPU x Margin %) / Churn &ge; 3.0x CAC
                    </p>
                  </div>
                  <div className="p-2.5 rounded-lg bg-white dark:bg-stone-950 border border-stone-200 dark:border-stone-800 font-mono">
                    <span className="text-[11px] font-bold text-emerald-600 dark:text-emerald-400 block mb-1">
                      Breakeven Volume (BEP)
                    </span>
                    <p className="text-[11px] text-stone-700 dark:text-stone-300">
                      BEP = Fixed Capex / Unit Contribution Margin
                    </p>
                  </div>
                </div>
              </div>

              {/* Documentation Assets */}
              <div className="p-4 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-900 text-white space-y-3">
                <div className="flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-cyan-400" />
                  <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-400">
                    Official System Documentation Assets
                  </h4>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  <div className="p-2.5 rounded-lg bg-stone-800/80 border border-stone-700/60">
                    <span className="font-semibold block text-stone-200">System Pipeline Guide (PDF)</span>
                    <span className="text-[10px] text-stone-400 font-mono">docs/CASE_COMPETITION_SYSTEM_PIPELINE_GUIDE.pdf</span>
                  </div>
                  <div className="p-2.5 rounded-lg bg-stone-800/80 border border-stone-700/60">
                    <span className="font-semibold block text-stone-200">How the Machine Works (Guide)</span>
                    <span className="text-[10px] text-stone-400 font-mono">docs/HOW_THE_CASE_MACHINE_WORKS.md</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

