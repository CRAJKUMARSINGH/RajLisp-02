import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { 
  Building2, 
  Ruler, 
  Road, 
  Stairs, 
  Bridge, 
  Sun, 
  Home,
  Menu,
  X,
  Settings,
  Download,
  Share2,
  HelpCircle
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { useTheme } from "@/components/theme-provider";

interface LayoutProps {
  children: React.ReactNode;
}

const navigationItems = [
  {
    title: "Dashboard",
    path: "/",
    icon: Home,
    color: "bg-blue-500",
    description: "Overview & Quick Actions"
  },
  {
    title: "Beam Design",
    path: "/beams",
    icon: Ruler,
    color: "bg-green-500",
    description: "L-Beam, T-Beam, Rectangular Beam",
    subItems: [
      { name: "L-Beam", path: "/beams?type=l-beam" },
      { name: "T-Beam", path: "/beams?type=t-beam" },
      { name: "Rectangular Beam", path: "/beams?type=rect-beam" }
    ]
  },
  {
    title: "Column Design",
    path: "/columns",
    icon: Building2,
    color: "bg-purple-500",
    description: "Circular & Rectangular Columns",
    subItems: [
      { name: "Circular Column", path: "/columns?type=circular" },
      { name: "Rectangular Column", path: "/columns?type=rectangular" }
    ]
  },
  {
    title: "Footing Design",
    path: "/footings",
    icon: Building2,
    color: "bg-orange-500",
    description: "Column Footings & Foundations",
    subItems: [
      { name: "Circular Footing", path: "/footings?type=circular" },
      { name: "Rectangular Footing", path: "/footings?type=rectangular" }
    ]
  },
  {
    title: "Road Design",
    path: "/roads",
    icon: Road,
    color: "bg-yellow-500",
    description: "Road Sections & Plans",
    subItems: [
      { name: "Road L-Section", path: "/roads?type=l-section" },
      { name: "Road Plan", path: "/roads?type=plan" },
      { name: "Road Cross Section", path: "/roads?type=cross-section" },
      { name: "PMGSY Road", path: "/roads?type=pmgsy" }
    ]
  },
  {
    title: "Staircase Design",
    path: "/staircases",
    icon: Stairs,
    color: "bg-red-500",
    description: "Various Staircase Configurations"
  },
  {
    title: "Bridge Design",
    path: "/bridges",
    icon: Bridge,
    color: "bg-indigo-500",
    description: "Bridge Components & Calculations"
  },
  {
    title: "Lintel Design",
    path: "/lintels",
    icon: Ruler,
    color: "bg-teal-500",
    description: "Lintel Beam Design"
  },
  {
    title: "Sunshade Design",
    path: "/sunshades",
    icon: Sun,
    color: "bg-amber-500",
    description: "Sunshade & Canopy Design"
  }
];

export default function Layout({ children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const { theme, setTheme } = useTheme();

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar */}
      <motion.aside
        initial={{ x: -300 }}
        animate={{ x: sidebarOpen ? 0 : -300 }}
        transition={{ type: "spring", damping: 20 }}
        className={`fixed left-0 top-0 z-50 h-full w-80 bg-card border-r border-border shadow-xl lg:translate-x-0 lg:static lg:z-auto ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="flex h-16 items-center justify-between px-6 border-b border-border">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Building2 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">RajLisp</h1>
                <p className="text-sm text-muted-foreground">Structural Suite</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleSidebar}
              className="lg:hidden"
            >
              <X className="w-5 h-5" />
            </Button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto px-4 py-6">
            <div className="space-y-2">
              {navigationItems.map((item) => {
                const isActive = location.pathname === item.path;
                const Icon = item.icon;
                
                return (
                  <div key={item.path}>
                    <Link
                      to={item.path}
                      className={`group flex items-center space-x-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200 ${
                        isActive
                          ? "bg-primary text-primary-foreground shadow-md"
                          : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                      }`}
                    >
                      <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${item.color} text-white`}>
                        <Icon className="w-4 h-4" />
                      </div>
                      <div className="flex-1">
                        <div className="font-medium">{item.title}</div>
                        <div className="text-xs opacity-75">{item.description}</div>
                      </div>
                      {isActive && (
                        <motion.div
                          layoutId="activeIndicator"
                          className="w-2 h-2 bg-primary-foreground rounded-full"
                        />
                      )}
                    </Link>
                    
                    {/* Sub-items */}
                    {item.subItems && isActive && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        className="ml-11 mt-2 space-y-1"
                      >
                        {item.subItems.map((subItem) => (
                          <Link
                            key={subItem.path}
                            to={subItem.path}
                            className="block px-3 py-2 text-sm text-muted-foreground hover:text-foreground hover:bg-accent rounded-md transition-colors"
                          >
                            {subItem.name}
                          </Link>
                        ))}
                      </motion.div>
                    )}
                  </div>
                );
              })}
            </div>
          </nav>

          {/* Footer */}
          <div className="border-t border-border p-4">
            <div className="flex items-center justify-between text-sm text-muted-foreground">
              <span>v1.0.0</span>
              <div className="flex space-x-2">
                <Button variant="ghost" size="sm">
                  <HelpCircle className="w-4 h-4" />
                </Button>
                <Button variant="ghost" size="sm">
                  <Settings className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </motion.aside>

      {/* Main Content */}
      <div className="lg:pl-80">
        {/* Top Header */}
        <header className="sticky top-0 z-30 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b border-border">
          <div className="flex h-16 items-center justify-between px-6">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleSidebar}
                className="lg:hidden"
              >
                <Menu className="w-5 h-5" />
              </Button>
              <div className="hidden md:block">
                <h2 className="text-lg font-semibold">
                  {navigationItems.find(item => item.path === location.pathname)?.title || "Dashboard"}
                </h2>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm">
                <Download className="w-4 h-4 mr-2" />
                Export
              </Button>
              <Button variant="outline" size="sm">
                <Share2 className="w-4 h-4 mr-2" />
                Share
              </Button>
              <Badge variant="secondary" className="hidden md:inline-flex">
                Engineering Mode
              </Badge>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
