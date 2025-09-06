import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Header } from "@/components/layout/header";
import { StaircaseCalculator } from "@/components/design-modules/staircase-calculator";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Calculator, FileText, Clock, CheckCircle } from "lucide-react";
import { Link } from "wouter";
import { formatDistanceToNow } from "date-fns";

interface StaircaseCalculation {
  id: number;
  projectId: number;
  inputData: any;
  results: any;
  createdAt: Date;
  isValid: string;
}

export default function StaircaseDesign() {
  const [showCalculator, setShowCalculator] = useState(false);

  const { data: calculations, isLoading } = useQuery<StaircaseCalculation[]>({
    queryKey: ['/api/user/1/calculations'],
    select: (data) => data?.filter((calc: any) => calc.type === 'staircase') || []
  });

  const handleNewCalculation = () => {
    setShowCalculator(true);
  };

  const handleCloseCalculator = () => {
    setShowCalculator(false);
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-4 mb-4">
            <Link href="/">
              <Button variant="outline" size="sm">
                <ArrowLeft className="mr-2" size={16} />
                Back to Dashboard
              </Button>
            </Link>
          </div>
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Staircase Design</h1>
              <p className="text-gray-600">RCC staircase design with waist slab calculations following IS-456:2000</p>
            </div>
            
            <Button onClick={handleNewCalculation} className="bg-primary hover:bg-blue-700">
              <Calculator className="mr-2" size={16} />
              New Calculation
            </Button>
          </div>
        </div>

        {/* Design Information */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <FileText className="mr-2 text-blue-600" size={20} />
                Design Standards
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <Badge className="bg-green-100 text-green-800">IS-456:2000</Badge>
                <p className="text-sm text-gray-600 mt-2">
                  Plain and Reinforced Concrete - Code of Practice
                </p>
                <Badge className="bg-blue-100 text-blue-800">IS-875:1987</Badge>
                <p className="text-sm text-gray-600 mt-2">
                  Code of Practice for Design Loads for Buildings and Structures
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <Calculator className="mr-2 text-green-600" size={20} />
                Calculation Features
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="text-green-600" size={14} />
                  <span>Load calculations (DL + LL)</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="text-green-600" size={14} />
                  <span>Bending moment analysis</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="text-green-600" size={14} />
                  <span>Reinforcement design</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="text-green-600" size={14} />
                  <span>Shear & deflection checks</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center">
                <Clock className="mr-2 text-orange-600" size={20} />
                Quick Stats
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div>
                  <p className="text-2xl font-bold text-gray-900">{calculations?.length || 0}</p>
                  <p className="text-sm text-gray-600">Total Calculations</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-gray-900">
                    {calculations?.filter(calc => calc.isValid === 'true').length || 0}
                  </p>
                  <p className="text-sm text-gray-600">Valid Designs</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Calculations */}
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">Recent Staircase Calculations</CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="animate-pulse">
                    <div className="flex items-center space-x-4 p-4 border border-gray-200 rounded-lg">
                      <div className="bg-gray-200 w-12 h-12 rounded"></div>
                      <div className="flex-1 space-y-2">
                        <div className="bg-gray-200 h-4 rounded w-3/4"></div>
                        <div className="bg-gray-200 h-3 rounded w-1/2"></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : calculations?.length === 0 ? (
              <div className="text-center py-12">
                <Calculator className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No calculations yet</h3>
                <p className="text-gray-600 mb-4">Create your first staircase design calculation to get started.</p>
                <Button onClick={handleNewCalculation} className="bg-primary hover:bg-blue-700">
                  <Calculator className="mr-2" size={16} />
                  Start New Calculation
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {calculations?.map((calculation) => (
                  <div key={calculation.id} className="border border-gray-200 rounded-lg p-4 hover:border-primary transition-colors">
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-4">
                        <div className="bg-blue-100 p-3 rounded-full">
                          <Calculator className="text-primary" size={20} />
                        </div>
                        <div>
                          <h3 className="font-medium text-gray-900">
                            Staircase Design - Project {calculation.projectId}
                          </h3>
                          <div className="mt-1 text-sm text-gray-600">
                            <p>Clear span: {calculation.inputData?.clearSpan}mm</p>
                            <p>Risers: {calculation.inputData?.numRisers} × {calculation.inputData?.riser}mm</p>
                            <p>Treads: {calculation.inputData?.tread}mm</p>
                          </div>
                          <div className="mt-2 flex items-center space-x-4">
                            <Badge 
                              className={calculation.isValid === 'true' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}
                            >
                              {calculation.isValid === 'true' ? 'Valid Design' : 'Needs Review'}
                            </Badge>
                            <span className="text-xs text-gray-400">
                              {formatDistanceToNow(new Date(calculation.createdAt), { addSuffix: true })}
                            </span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <Button variant="outline" size="sm">
                          <FileText className="mr-1" size={14} />
                          Report
                        </Button>
                        <Button variant="outline" size="sm">
                          View Details
                        </Button>
                      </div>
                    </div>
                    
                    {calculation.results && (
                      <div className="mt-4 pt-4 border-t border-gray-100">
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                          <div>
                            <p className="text-xs text-gray-500">Max Moment</p>
                            <p className="font-medium">{calculation.results.maxMoment} kN.m</p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-500">Main Steel</p>
                            <p className="font-medium">{calculation.results.mainSteelArea} mm²</p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-500">Bar Spacing</p>
                            <p className="font-medium">{calculation.results.providedSpacing}mm c/c</p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-500">Slab Thickness</p>
                            <p className="font-medium">{calculation.results.waistThickness}mm</p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Calculator Modal */}
      {showCalculator && (
        <StaircaseCalculator onClose={handleCloseCalculator} />
      )}
    </div>
  );
}
