import { BarChart3, Bot, Leaf, PanelLeftClose, ShieldCheck, Factory, Upload, Building2, MessageSquare, FlaskConical, Scale } from "lucide-react"
import { NavLink } from "react-router-dom"
import { useState, type ReactNode } from "react"

type AppShellProps = {
  children: ReactNode
}

const navItems = [
  { to: "/reference-dashboard", label: "Reference Dashboard", icon: BarChart3, end: false },
  { to: "/company-dashboard", label: "Company Dashboard", icon: Building2, end: false },
  { to: "/benchmark", label: "Benchmark", icon: Scale, end: false },
  { to: "/carbon", label: "Carbon", icon: Factory, end: false },
  { to: "/upload-center", label: "Upload Center", icon: Upload, end: false },
  { to: "/ai-analysis", label: "AI Analiz", icon: Bot, end: false },
  { to: "/ai-chatbox", label: "AI Chatbox", icon: MessageSquare, end: false },
  { to: "/scenario-simulation", label: "Scenario Simulation", icon: FlaskConical, end: false },
]

export default function AppShell({ children }: AppShellProps) {
  const [collapsed, setCollapsed] = useState(false)

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="flex min-h-screen">
        <aside
          className={`${collapsed ? "w-24" : "w-72"} hidden border-r border-slate-200 bg-[#0F172A] text-white transition-all duration-300 lg:flex lg:flex-col`}
        >
          <div className="flex items-center justify-between border-b border-white/10 px-5 py-5">
            <div className={`${collapsed ? "hidden" : "block"}`}>
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-teal-300">
                Sustainability
              </p>
              <h1 className="mt-1 text-xl font-bold">Carbon Insight Hub</h1>
            </div>

            <button
              onClick={() => setCollapsed(!collapsed)}
              className="rounded-xl border border-white/10 bg-white/5 p-2 text-slate-200 transition hover:bg-white/10"
            >
              <PanelLeftClose size={18} />
            </button>
          </div>

          <div className="px-4 py-5">
            <div className="mb-5 rounded-2xl border border-teal-400/20 bg-gradient-to-br from-teal-600/20 to-emerald-500/10 p-4">
              <div className="flex items-center gap-3">
                <div className="rounded-2xl bg-teal-500/20 p-3 text-teal-200">
                  <Leaf size={20} />
                </div>
                {!collapsed && (
                  <div>
                    <p className="text-sm font-semibold">Industrial Sustainability</p>
                    <p className="text-xs text-slate-300">
                      Analytics & Decision Support
                    </p>
                  </div>
                )}
              </div>
            </div>

            <nav className="space-y-2">
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    end={item.end}
                    className={({ isActive }) =>
                      [
                        "flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition",
                        isActive
                          ? "bg-teal-600 text-white shadow-lg shadow-teal-900/20"
                          : "text-slate-300 hover:bg-white/8 hover:text-white",
                      ].join(" ")
                    }
                  >
                    <Icon size={18} />
                    {!collapsed && <span>{item.label}</span>}
                  </NavLink>
                )
              })}
            </nav>
          </div>

          <div className="mt-auto px-4 pb-5">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="flex items-start gap-3">
                <div className="rounded-xl bg-emerald-500/15 p-2 text-emerald-300">
                  <ShieldCheck size={18} />
                </div>
                {!collapsed && (
                  <div>
                    <p className="text-sm font-semibold">MVP+</p>
                    <p className="mt-1 text-xs leading-5 text-slate-300">
                      Dashboard, benchmark, AI analiz, chatbox ve senaryo modülü birlikte çalışıyor.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </aside>

        <div className="flex min-h-screen flex-1 flex-col">
          <header className="border-b border-slate-200 bg-white/85 px-6 py-4 backdrop-blur">
            <div className="mx-auto flex max-w-7xl items-center justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">
                  Industrial Sustainability Platform
                </p>
                <h2 className="mt-1 text-2xl font-bold tracking-tight text-slate-900">
                  Decision Support Dashboard
                </h2>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-2 text-sm text-slate-600">
                GHGRP • eGRID • Company Data
              </div>
            </div>
          </header>

          <main className="flex-1 px-6 py-6">
            <div className="mx-auto max-w-7xl">{children}</div>
          </main>
        </div>
      </div>
    </div>
  )
}
