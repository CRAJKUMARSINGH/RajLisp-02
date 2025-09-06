import { Link, useLocation } from "wouter";
import { Calculator, Bell, User } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Header() {
  const [location] = useLocation();

  const navItems = [
    { path: "/", label: "Dashboard", active: location === "/" },
    { path: "/projects", label: "Projects", active: location === "/projects" },
    { path: "/reports", label: "Reports", active: location === "/reports" },
    { path: "/settings", label: "Settings", active: location === "/settings" }
  ];

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-4">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary rounded flex items-center justify-center">
                <Calculator className="text-white" size={16} />
              </div>
              <h1 className="text-xl font-bold text-gray-900">StructuralCAD Pro</h1>
            </Link>
            <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">v2.1.0</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <nav className="hidden md:flex space-x-8">
              {navItems.map((item) => (
                <Link key={item.path} href={item.path}>
                  <button
                    className={`font-medium text-sm ${
                      item.active 
                        ? "text-primary border-b-2 border-primary pb-1" 
                        : "text-gray-600 hover:text-primary"
                    }`}
                  >
                    {item.label}
                  </button>
                </Link>
              ))}
            </nav>
            
            <div className="flex items-center space-x-2">
              <Button variant="ghost" size="icon" className="text-gray-600 hover:text-primary hover:bg-gray-100 rounded p-2">
                <Bell size={20} />
              </Button>
              <div className="flex items-center space-x-2 bg-gray-100 rounded-full px-3 py-1">
                <User className="text-gray-600" size={16} />
                <span className="text-sm font-medium text-gray-700">Nirmal Suthar</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
