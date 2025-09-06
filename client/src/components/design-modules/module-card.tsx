import { DesignModule } from "@/types/structural";
import { Badge } from "@/components/ui/badge";

interface ModuleCardProps {
  module: DesignModule;
  onClick: () => void;
}

export function ModuleCard({ module, onClick }: ModuleCardProps) {
  const isComingSoon = module.status === 'coming-soon';
  
  const getIconElement = (iconName: string) => {
    const iconMap: Record<string, string> = {
      "stairs": "🔸",
      "view_column": "⬜", 
      "horizontal_rule": "▬",
      "foundation": "🏗️",
    };
    return iconMap[iconName] || iconName;
  };

  const colorClasses = {
    blue: "bg-blue-50 group-hover:bg-blue-100 text-primary",
    green: "bg-green-50 group-hover:bg-green-100 text-accent",
    purple: "bg-purple-50 group-hover:bg-purple-100 text-purple-600",
    orange: "bg-orange-50 group-hover:bg-orange-100 text-orange-600",
  }[module.color] || "bg-gray-50 group-hover:bg-gray-100 text-gray-600";

  if (isComingSoon) {
    return (
      <div className="border border-gray-200 rounded-lg p-4 bg-gray-50 opacity-60">
        <div className="flex items-start space-x-3">
          <div className="bg-gray-100 p-2 rounded">
            <span className="text-gray-400">{getIconElement(module.icon)}</span>
          </div>
          <div className="flex-1">
            <h4 className="font-medium text-gray-400">{module.name}</h4>
            <p className="text-sm text-gray-400 mt-1">{module.description}</p>
            <div className="flex items-center mt-2">
              <Badge variant="secondary" className="text-xs">Coming Soon</Badge>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div 
      className="border border-gray-200 rounded-lg p-4 hover:border-primary hover:shadow-md transition-all cursor-pointer group"
      onClick={onClick}
    >
      <div className="flex items-start space-x-3">
        <div className={`p-2 rounded ${colorClasses}`}>
          <span>{getIconElement(module.icon)}</span>
        </div>
        <div className="flex-1">
          <h4 className="font-medium text-gray-900 group-hover:text-primary">{module.name}</h4>
          <p className="text-sm text-gray-600 mt-1">{module.description}</p>
          <div className="flex items-center mt-2 space-x-4">
            {module.standards.map((standard) => (
              <Badge key={standard} variant="secondary" className="text-xs bg-green-100 text-green-800">
                {standard}
              </Badge>
            ))}
            {module.lastUsed && (
              <span className="text-xs text-gray-500">{module.lastUsed}</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
