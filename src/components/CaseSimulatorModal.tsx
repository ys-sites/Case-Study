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
} from 'lucide-react';
import solutionData from '../data/current_case_solution.json';
import sampleCases from '../data/case_index.json';

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
  const [activeTab, setActiveTab] = useState<'solution' | 'financials' | 'defense' | 'video' | 'agents' | 'architecture'>('solution');
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
        <div className="flex border-b border-stone-200 dark:border-stone-800 bg-stone-100 dark:bg-stone-900 px-6 gap-2 pt-2">
          {[
            { id: 'solution', label: 'Winning Solution', icon: Award },
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
        <div className="flex-1 overflow-y-auto p-6 bg-white dark:bg-stone-950">
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
              <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
                <h3 className="font-bold text-sm text-stone-900 dark:text-stone-100">
                  2-Minute Demonstration Video & Deliverables Package
                </h3>
                <p className="text-xs text-stone-600 dark:text-stone-300 mt-1">
                  Rendered MP4 (1080p), 12-slide executive presentation, and 2 verified PDF reports.
                </p>
              </div>

              {/* Video Player Card */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-2xl border border-stone-200 dark:border-stone-800 bg-stone-950 text-white flex flex-col items-center justify-center min-h-[200px]">
                  <Video className="w-10 h-10 text-cyan-400 mb-2 animate-pulse" />
                  <h4 className="text-sm font-bold text-center">System Architecture Explainer (112s)</h4>
                  <p className="text-[11px] text-stone-400 mt-1 text-center">
                    Finished Resources/09_Video/System_Architecture_Explainer.mp4<br/>
                    1080p | Neural Voiceover + Procedural Ambience
                  </p>
                </div>
                <div className="p-4 rounded-2xl border border-stone-200 dark:border-stone-800 bg-stone-950 text-white flex flex-col items-center justify-center min-h-[200px]">
                  <Video className="w-10 h-10 text-amber-500 mb-2 animate-pulse" />
                  <h4 className="text-sm font-bold text-center">Case Solution Demo Video (120s)</h4>
                  <p className="text-[11px] text-stone-400 mt-1 text-center">
                    Finished Resources/09_Video/Final_Demo_120s.mp4<br/>
                    1080p | Synchronized Storyboard & Subtitles (.srt)
                  </p>
                </div>
              </div>

              {/* Direct Deliverable Files */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="p-3.5 rounded-xl border border-cyan-500/30 bg-cyan-500/5 dark:bg-cyan-950/20 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2.5">
                    <FileText className="w-4 h-4 text-cyan-500" />
                    <div>
                      <div className="font-semibold text-stone-900 dark:text-stone-100">System_Pipeline_Guide.pdf</div>
                      <div className="text-[11px] text-stone-400">docs/CASE_COMPETITION_SYSTEM_PIPELINE_GUIDE.pdf</div>
                    </div>
                  </div>
                  <span className="font-mono text-cyan-600 dark:text-cyan-400 font-bold">6 Pages Ready</span>
                </div>

                <div className="p-3.5 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2.5">
                    <FileText className="w-4 h-4 text-rose-500" />
                    <div>
                      <div className="font-semibold text-stone-900 dark:text-stone-100">Strategic_Blueprint.pdf</div>
                      <div className="text-[11px] text-stone-400">Finished Resources/06_PDF_Deliverables</div>
                    </div>
                  </div>
                  <span className="font-mono text-emerald-600 font-bold">Ready</span>
                </div>

                <div className="p-3.5 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2.5">
                    <FileText className="w-4 h-4 text-rose-500" />
                    <div>
                      <div className="font-semibold text-stone-900 dark:text-stone-100">Final_Case_Solution.pdf</div>
                      <div className="text-[11px] text-stone-400">Finished Resources/06_PDF_Deliverables</div>
                    </div>
                  </div>
                  <span className="font-mono text-emerald-600 font-bold">Ready</span>
                </div>

                <div className="p-3.5 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2.5">
                    <PresentationIcon className="w-4 h-4 text-amber-500" />
                    <div>
                      <div className="font-semibold text-stone-900 dark:text-stone-100">Final_Presentation.pptx</div>
                      <div className="text-[11px] text-stone-400">12 Slides | Finished Resources/07_PowerPoint</div>
                    </div>
                  </div>
                  <span className="font-mono text-emerald-600 font-bold">Ready</span>
                </div>

                <div className="p-3.5 rounded-xl border border-stone-200 dark:border-stone-800 bg-stone-50 dark:bg-stone-900 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2.5">
                    <Calculator className="w-4 h-4 text-emerald-500" />
                    <div>
                      <div className="font-semibold text-stone-900 dark:text-stone-100">financial_model.xlsx</div>
                      <div className="text-[11px] text-stone-400">Finished Resources/05_Financial_Models</div>
                    </div>
                  </div>
                  <span className="font-mono text-emerald-600 font-bold">Ready</span>
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

