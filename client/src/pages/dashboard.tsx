import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { 
  Building2, 
  Ruler, 
  Road, 
  Stairs, 
  Bridge, 
  Sun, 
  Calculator,
  FileText,
  Download,
  Share2,
  TrendingUp,
  Clock,
  Star,
  Zap
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

const quickActions = [
  {
    title: "L-Beam Design",
    description: "Design L-shaped reinforced concrete beams",
    icon: Ruler,
    color: "bg-green-500",
    path: "/beams?type=l-beam",
    complexity: "Medium"
  },
  {
    title: "Circular Column",
    description: "Design circular reinforced concrete columns",
    icon: Building2,
    color: "bg-purple-500",
    path: "/columns?type=circular",
    complexity: "Easy"
  },
  {
    title: "Road Section",
    description: "Generate road cross-sectional drawings",
    icon: Road,
    color: "bg-yellow-500",
    path: "/roads?type=l-section",
    complexity: "Medium"
  },
  {
    title: "Staircase",
    description: "Design various staircase configurations",
    icon: Stairs,
    color: "bg-red-500",
    path: "/staircases",
    complexity: "Hard"
  },
  {
    title: "Bridge Design",
    description: "Bridge component calculations",
    icon: Bridge,
    color: "bg-indigo-500",
    path: "/bridges",
    complexity: "Hard"
  },
  {
    title: "Sunshade",
    description: "Design sunshade and canopy structures",
    icon: Sun,
    color: "bg-amber-500",
    path: "/sunshades",
    complexity: "Medium"
  }
];

const recentProjects = [
  {
    name: "Residential Building - Beam Design",
    type: "L-Beam",
    date: "2 hours ago",
    status: "Completed",
    progress: 100
  },
  {
    name: "Commercial Complex - Column Design",
    type: "Circular Column",
    date: "1 day ago",
    status: "In Progress",
    progress: 75
  },
  {
    name: "Highway Project - Road Section",
    type: "Road Design",
    date: "3 days ago",
    status: "Completed",
    progress: 100
  }
];

const stats = [
  {
    title: "Total Designs",
    value: "47",
    change: "+12%",
    trend: "up"
  },
  {
    title: "Active Projects",
    value: "8",
    change: "+3",
    trend: "up"
  },
  {
    title: "Time Saved",
    value: "23h",
    change: "+5h",
    trend: "up"
  },
  {
    title: "Success Rate",
    value: "94%",
    change: "+2%",
    trend: "up"
  }
];

export default function Dashboard() {
  const [selectedAction, setSelectedAction] = useState<string | null>(null);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <motion.h1 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold tracking-tight"
        >
          Welcome to RajLisp Structural Suite
        </motion.h1>
        <motion.p 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-xl text-muted-foreground"
        >
          Professional structural engineering design and drafting platform
        </motion.p>
      </div>

      {/* Stats Grid */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {stats.map((stat, index) => (
          <Card key={stat.title} className="relative overflow-hidden">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">
                    {stat.title}
                  </p>
                  <p className="text-3xl font-bold">{stat.value}</p>
                </div>
                <div className={`text-sm font-medium ${
                  stat.trend === 'up' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {stat.change}
                </div>
              </div>
            </CardContent>
            <div className={`absolute bottom-0 left-0 right-0 h-1 ${
              stat.trend === 'up' ? 'bg-green-500' : 'bg-red-500'
            }`} />
          </Card>
        ))}
      </motion.div>

      {/* Quick Actions */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="space-y-4"
      >
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold">Quick Actions</h2>
          <Button variant="outline" size="sm">
            <Zap className="w-4 h-4 mr-2" />
            View All
          </Button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {quickActions.map((action, index) => (
            <motion.div
              key={action.title}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 * index }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <Link to={action.path}>
                <Card className="h-full cursor-pointer transition-all duration-200 hover:shadow-lg hover:border-primary/50">
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${action.color} text-white`}>
                        <action.icon className="w-6 h-6" />
                      </div>
                      <Badge variant="secondary" className="text-xs">
                        {action.complexity}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <CardTitle className="text-lg mb-2">{action.title}</CardTitle>
                    <CardDescription className="text-sm">
                      {action.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              </Link>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Recent Projects & Quick Tools */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Projects */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="space-y-4"
        >
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-semibold">Recent Projects</h2>
            <Button variant="ghost" size="sm">View All</Button>
          </div>
          
          <Card>
            <CardContent className="p-6">
              <div className="space-y-4">
                {recentProjects.map((project, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-1">
                        <h4 className="font-medium">{project.name}</h4>
                        <Badge variant="outline" className="text-xs">
                          {project.type}
                        </Badge>
                      </div>
                      <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                        <span className="flex items-center">
                          <Clock className="w-3 h-3 mr-1" />
                          {project.date}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          project.status === 'Completed' 
                            ? 'bg-green-100 text-green-700' 
                            : 'bg-yellow-100 text-yellow-700'
                        }`}>
                          {project.status}
                        </span>
                      </div>
                    </div>
                    <div className="w-20">
                      <Progress value={project.progress} className="h-2" />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Quick Tools */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="space-y-4"
        >
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-semibold">Quick Tools</h2>
          </div>
          
          <div className="space-y-3">
            <Card className="cursor-pointer hover:shadow-md transition-shadow">
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Calculator className="w-5 h-5 text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium">Unit Converter</h4>
                    <p className="text-sm text-muted-foreground">Convert between different units</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="cursor-pointer hover:shadow-md transition-shadow">
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                    <FileText className="w-5 h-5 text-green-600" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium">Report Generator</h4>
                    <p className="text-sm text-muted-foreground">Generate design reports</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="cursor-pointer hover:shadow-md transition-shadow">
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                    <Download className="w-5 h-5 text-purple-600" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium">Export Options</h4>
                    <p className="text-sm text-muted-foreground">Export to PDF, DWG, or DXF</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </motion.div>
      </div>

      {/* Features Highlight */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-8 border border-blue-200"
      >
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto">
            <Star className="w-8 h-8 text-white" />
          </div>
          <h3 className="text-2xl font-semibold text-gray-900">
            Professional Engineering Suite
          </h3>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Built on decades of engineering expertise, RajLisp Structural Suite provides 
            professional-grade design tools with modern web technology. Generate accurate 
            structural drawings, perform calculations, and create detailed documentation 
            all in one platform.
          </p>
          <div className="flex items-center justify-center space-x-4 text-sm text-gray-500">
            <span className="flex items-center">
              <Building2 className="w-4 h-4 mr-1" />
              Structural Design
            </span>
            <span className="flex items-center">
              <Ruler className="w-4 h-4 mr-1" />
              Auto CAD Integration
            </span>
            <span className="flex items-center">
              <Calculator className="w-4 h-4 mr-1" />
              Real-time Calculations
            </span>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
