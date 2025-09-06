import { useQuery } from "@tanstack/react-query";
import { Calculator, FileText, Building2 } from "lucide-react";
import { formatDistanceToNow } from "date-fns";

interface ActivityItem {
  id: number;
  type: string;
  projectId: number;
  createdAt: Date;
  inputData: any;
}

export function RecentActivity() {
  const { data: activities, isLoading } = useQuery({
    queryKey: ['/api/user/1/calculations'],
  });

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="animate-pulse">
                <div className="flex items-start space-x-3">
                  <div className="bg-gray-200 p-2 rounded-full w-8 h-8"></div>
                  <div className="flex-1 space-y-2">
                    <div className="bg-gray-200 h-4 rounded w-3/4"></div>
                    <div className="bg-gray-200 h-3 rounded w-1/2"></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'staircase': return Calculator;
      case 'beam': return Building2;
      case 'column': return Building2;
      default: return FileText;
    }
  };

  const getActivityColor = (type: string) => {
    switch (type) {
      case 'staircase': return 'bg-blue-100 text-blue-600';
      case 'beam': return 'bg-purple-100 text-purple-600';
      case 'column': return 'bg-green-100 text-green-600';
      default: return 'bg-gray-100 text-gray-600';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
      </div>
      <div className="p-6">
        <div className="space-y-4">
          {!activities || activities.length === 0 ? (
            <p className="text-gray-500 text-sm">No recent activity</p>
          ) : (
            activities.map((activity: ActivityItem) => {
              const Icon = getActivityIcon(activity.type);
              const colorClass = getActivityColor(activity.type);
              
              return (
                <div key={activity.id} className="flex items-start space-x-3 pb-4 border-b border-gray-100 last:border-b-0 last:pb-0">
                  <div className={`p-2 rounded-full flex-shrink-0 ${colorClass}`}>
                    <Icon size={16} />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">
                      {activity.type.charAt(0).toUpperCase() + activity.type.slice(1)} Design - Project {activity.projectId}
                    </p>
                    <p className="text-xs text-gray-600">
                      Calculation completed successfully
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      {formatDistanceToNow(new Date(activity.createdAt), { addSuffix: true })}
                    </p>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
