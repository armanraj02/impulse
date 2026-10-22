import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Building2, 
  AlertTriangle, 
  GraduationCap, 
  Lightbulb, 
  FileText,
  X,
  Activity,
  BookOpen,
  Calendar,
  Layers
} from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: (isOpen: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, setIsOpen }) => {
  const navItems = [
    { title: 'Dashboard', items: [{ name: 'Executive Overview', path: '/dashboard', icon: LayoutDashboard }] },
    { title: 'Performance', items: [
      { name: 'Department Performance', path: '/departments', icon: Building2 }
    ]},
    {
      title: 'Academics',
      items: [
        { name: 'Course & Feedback', icon: BookOpen, path: '/courses-feedback' },
        { name: 'Attendance Intelligence', icon: Calendar, path: '/attendance' },
        { name: 'Academic Intelligence', icon: GraduationCap, path: '/academic' },
        { name: 'Batch & Section', icon: Layers, path: '/batches-sections' },
      ]
    },
    { title: 'Intelligence', items: [
      { name: 'Student Risk', path: '/students/risk', icon: AlertTriangle },
      { name: 'Insights & Recommendations', path: '/insights', icon: Lightbulb }
    ]},
    { title: 'Reports', items: [{ name: 'Reports', path: '/reports', icon: FileText }] }
  ];

  return (
    <>
      <div 
        className={cn(
          "fixed inset-0 bg-slate-900/50 z-20 lg:hidden transition-opacity",
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        )}
        onClick={() => setIsOpen(false)}
      />
      
      <div className={cn(
        "fixed inset-y-0 left-0 z-30 w-64 bg-white border-r border-slate-200 transform transition-transform duration-300 lg:translate-x-0 lg:static lg:inset-0 flex flex-col",
        isOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="flex items-center justify-between h-16 px-6 border-b border-slate-200">
          <div className="flex items-center gap-2">
            <Activity className="w-6 h-6 text-brand-600" />
            <span className="text-xl font-bold text-slate-800 tracking-tight">INPULSE</span>
          </div>
          <button className="lg:hidden text-slate-500 hover:text-slate-700" onClick={() => setIsOpen(false)}>
            <X className="w-5 h-5" />
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-6">
          {navItems.map((section, idx) => (
            <div key={idx}>
              <h3 className="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
                {section.title}
              </h3>
              <div className="space-y-1">
                {section.items.map((item) => (
                  <NavLink
                    key={item.name}
                    to={item.path}
                    className={({ isActive }) => cn(
                      "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                      isActive 
                        ? "bg-brand-50 text-brand-700" 
                        : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                    )}
                  >
                    <item.icon className="w-4 h-4" />
                    {item.name}
                  </NavLink>
                ))}
              </div>
            </div>
          ))}
        </nav>
      </div>
    </>
  );
};

export default Sidebar;
