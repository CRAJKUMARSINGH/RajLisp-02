import { Plus, Upload, HelpCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

export function QuickActions() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
      </div>
      <div className="p-6 space-y-3">
        <Button 
          variant="outline" 
          className="w-full justify-start bg-blue-50 hover:bg-blue-100 border-blue-200"
        >
          <Plus className="mr-3" size={16} />
          New Project
        </Button>
        
        <Button 
          variant="outline" 
          className="w-full justify-start bg-gray-50 hover:bg-gray-100"
        >
          <Upload className="mr-3" size={16} />
          Import Data
        </Button>
        
        <Button 
          variant="outline" 
          className="w-full justify-start bg-gray-50 hover:bg-gray-100"
        >
          <HelpCircle className="mr-3" size={16} />
          Design Guide
        </Button>
      </div>
    </div>
  );
}
