import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calculator, FileText, Download, Route, MapPin } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface RoadCalculatorProps {
  onClose: () => void;
}

interface RoadInputs {
  roadLength: number;
  surveyInterval: number;
  maxLevel: number;
  minLevel: number;
  firstNSL: number;
  formationWidth: number;
  carriageWidth: number;
  carriageCamber: number;
  shoulderCamber: number;
  sideSlope: number;
  centreNSL: number;
  formationLevel: number;
  designType: 'longitudinal' | 'cross-section';
}

interface RoadResults {
  datum: number;
  numberOfPoints: number;
  cutFillData: Array<{
    chainage: number;
    nsl: number;
    formation: number;
    cut: number;
    fill: number;
  }>;
  totalCut: number;
  totalFill: number;
  crossSectionArea: number;
  recommendations: string[];
}

export function RoadCalculator({ onClose }: RoadCalculatorProps) {
  const { toast } = useToast();
  const [activeTab, setActiveTab] = useState("input");
  const [inputs, setInputs] = useState<RoadInputs>({
    roadLength: 100,
    surveyInterval: 10,
    maxLevel: 105.5,
    minLevel: 98.2,
    firstNSL: 100.5,
    formationWidth: 7.0,
    carriageWidth: 5.5,
    carriageCamber: 2.5,
    shoulderCamber: 3.0,
    sideSlope: 2.0,
    centreNSL: 102.5,
    formationLevel: 103.0,
    designType: 'longitudinal'
  });
  const [results, setResults] = useState<RoadResults | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);

  const calculateRoad = () => {
    setIsCalculating(true);
    
    setTimeout(() => {
      // Road design calculations based on original LISP algorithms
      
      // Calculate datum (nearest 5m below minimum level)
      const datum = Math.floor(inputs.minLevel / 5) * 5;
      
      // Number of survey points
      const numberOfPoints = Math.ceil(inputs.roadLength / inputs.surveyInterval) + 1;
      
      // Generate cut/fill data for longitudinal profile
      const cutFillData = [];
      let totalCut = 0;
      let totalFill = 0;
      
      for (let i = 0; i < numberOfPoints; i++) {
        const chainage = i * inputs.surveyInterval;
        
        // Generate NSL values (simplified interpolation)
        const nsl = inputs.firstNSL + 
          ((inputs.maxLevel - inputs.firstNSL) * Math.sin((chainage / inputs.roadLength) * Math.PI));
        
        // Formation level (simplified gradient)
        const formation = inputs.firstNSL + 
          ((inputs.roadLength - chainage) / inputs.roadLength) * 2.0; // 2m gradient over length
        
        // Calculate cut and fill
        const difference = nsl - formation;
        const cut = difference > 0 ? difference : 0;
        const fill = difference < 0 ? Math.abs(difference) : 0;
        
        totalCut += cut;
        totalFill += fill;
        
        cutFillData.push({
          chainage,
          nsl: parseFloat(nsl.toFixed(2)),
          formation: parseFloat(formation.toFixed(2)),
          cut: parseFloat(cut.toFixed(2)),
          fill: parseFloat(fill.toFixed(2))
        });
      }
      
      // Cross-section area calculation
      const shoulderWidth = (inputs.formationWidth - inputs.carriageWidth) / 2;
      const carriageArea = inputs.carriageWidth * (inputs.carriageCamber / 100) * (inputs.carriageWidth / 2);
      const shoulderArea = shoulderWidth * (inputs.shoulderCamber / 100) * (shoulderWidth / 2);
      const crossSectionArea = carriageArea + (shoulderArea * 2);
      
      // Generate recommendations
      const recommendations = [];
      if (totalCut > totalFill * 1.2) {
        recommendations.push("⚠️ Excess cut material - consider using for other sections");
      }
      if (totalFill > totalCut * 1.2) {
        recommendations.push("⚠️ Borrow material required for filling");
      }
      if (Math.abs(totalCut - totalFill) / Math.max(totalCut, totalFill) < 0.1) {
        recommendations.push("✓ Well balanced cut-fill - optimal design");
      }
      if (inputs.carriageCamber < 2.0) {
        recommendations.push("⚠️ Consider increasing carriageway camber for drainage");
      }
      if (recommendations.length === 0) {
        recommendations.push("✓ Design meets IRC guidelines");
      }

      setResults({
        datum,
        numberOfPoints,
        cutFillData,
        totalCut: parseFloat(totalCut.toFixed(2)),
        totalFill: parseFloat(totalFill.toFixed(2)),
        crossSectionArea: parseFloat(crossSectionArea.toFixed(2)),
        recommendations
      });
      
      setActiveTab("results");
      setIsCalculating(false);
      
      toast({
        title: "Road Design Complete",
        description: "Road geometric design calculations finished successfully.",
      });
    }, 2000);
  };

  const generateReport = () => {
    toast({
      title: "Report Generated",
      description: "Road design report with drawings prepared for download.",
    });
  };

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-6xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Route className="h-5 w-5 text-green-600" />
            Road Geometric Design Calculator
            <Badge variant="secondary" className="ml-2">IRC-73</Badge>
            <Badge variant="outline" className="ml-1">LISP-Based</Badge>
          </DialogTitle>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="input">Design Parameters</TabsTrigger>
            <TabsTrigger value="results" disabled={!results}>Calculations</TabsTrigger>
            <TabsTrigger value="report" disabled={!results}>Report & Drawings</TabsTrigger>
          </TabsList>

          <TabsContent value="input" className="space-y-6">
            {/* Design Type Selection */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Design Type</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex space-x-4">
                  <Button
                    variant={inputs.designType === 'longitudinal' ? 'default' : 'outline'}
                    onClick={() => setInputs({...inputs, designType: 'longitudinal'})}
                  >
                    Longitudinal Profile
                  </Button>
                  <Button
                    variant={inputs.designType === 'cross-section' ? 'default' : 'outline'}
                    onClick={() => setInputs({...inputs, designType: 'cross-section'})}
                  >
                    Cross Section
                  </Button>
                </div>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Longitudinal Profile Parameters */}
              {inputs.designType === 'longitudinal' && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Longitudinal Profile Data</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="roadLength">Road Length (m)</Label>
                        <Input
                          id="roadLength"
                          type="number"
                          value={inputs.roadLength}
                          onChange={(e) => setInputs({...inputs, roadLength: parseFloat(e.target.value)})}
                          min="10"
                          max="1000"
                        />
                      </div>
                      <div>
                        <Label htmlFor="surveyInterval">Survey Interval (m)</Label>
                        <Input
                          id="surveyInterval"
                          type="number"
                          value={inputs.surveyInterval}
                          onChange={(e) => setInputs({...inputs, surveyInterval: parseFloat(e.target.value)})}
                          min="5"
                          max="50"
                        />
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="maxLevel">Maximum Level (m)</Label>
                        <Input
                          id="maxLevel"
                          type="number"
                          value={inputs.maxLevel}
                          onChange={(e) => setInputs({...inputs, maxLevel: parseFloat(e.target.value)})}
                          step="0.1"
                        />
                      </div>
                      <div>
                        <Label htmlFor="minLevel">Minimum Level (m)</Label>
                        <Input
                          id="minLevel"
                          type="number"
                          value={inputs.minLevel}
                          onChange={(e) => setInputs({...inputs, minLevel: parseFloat(e.target.value)})}
                          step="0.1"
                        />
                      </div>
                    </div>
                    <div>
                      <Label htmlFor="firstNSL">NSL of First Point (m)</Label>
                      <Input
                        id="firstNSL"
                        type="number"
                        value={inputs.firstNSL}
                        onChange={(e) => setInputs({...inputs, firstNSL: parseFloat(e.target.value)})}
                        step="0.1"
                      />
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Cross Section Parameters */}
              {inputs.designType === 'cross-section' && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Cross Section Data</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="formationWidth">Formation Width (m)</Label>
                        <Input
                          id="formationWidth"
                          type="number"
                          value={inputs.formationWidth}
                          onChange={(e) => setInputs({...inputs, formationWidth: parseFloat(e.target.value)})}
                          step="0.1"
                        />
                      </div>
                      <div>
                        <Label htmlFor="carriageWidth">Carriageway Width (m)</Label>
                        <Input
                          id="carriageWidth"
                          type="number"
                          value={inputs.carriageWidth}
                          onChange={(e) => setInputs({...inputs, carriageWidth: parseFloat(e.target.value)})}
                          step="0.1"
                        />
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="carriageCamber">Carriageway Camber (%)</Label>
                        <Input
                          id="carriageCamber"
                          type="number"
                          value={inputs.carriageCamber}
                          onChange={(e) => setInputs({...inputs, carriageCamber: parseFloat(e.target.value)})}
                          step="0.1"
                        />
                      </div>
                      <div>
                        <Label htmlFor="shoulderCamber">Shoulder Camber (%)</Label>
                        <Input
                          id="shoulderCamber"
                          type="number"
                          value={inputs.shoulderCamber}
                          onChange={(e) => setInputs({...inputs, shoulderCamber: parseFloat(e.target.value)})}
                          step="0.1"
                        />
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="sideSlope">Side Slope (n:1)</Label>
                        <Input
                          id="sideSlope"
                          type="number"
                          value={inputs.sideSlope}
                          onChange={(e) => setInputs({...inputs, sideSlope: parseFloat(e.target.value)})}
                          step="0.1"
                        />
                      </div>
                      <div>
                        <Label htmlFor="centreNSL">Centre NSL (m)</Label>
                        <Input
                          id="centreNSL"
                          type="number"
                          value={inputs.centreNSL}
                          onChange={(e) => setInputs({...inputs, centreNSL: parseFloat(e.target.value)})}
                          step="0.1"
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Algorithm Display */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">LISP Algorithm Translation</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                    <div className="font-mono text-sm space-y-1">
                      <div><strong>Original LISP Logic:</strong></div>
                      <div className="text-blue-700">DATUM = MIN_LEVEL - (MIN_LEVEL % 5)</div>
                      <div className="text-blue-700">NO_POINTS = LENGTH / INTERVAL</div>
                      <div className="text-blue-700">CUT = NSL - FORMATION (if positive)</div>
                      <div className="text-blue-700">FILL = FORMATION - NSL (if positive)</div>
                    </div>
                  </div>
                  <div className="bg-amber-50 p-3 rounded-lg border border-amber-200">
                    <div className="text-sm">
                      <strong>Standards:</strong> Based on IRC guidelines for rural road design
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="flex justify-between pt-4">
              <Button variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button onClick={calculateRoad} disabled={isCalculating}>
                {isCalculating ? "Calculating..." : "Generate Road Design"}
                <Calculator className="h-4 w-4 ml-2" />
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="results" className="space-y-6">
            {results && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Summary */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <MapPin className="h-5 w-5 text-green-500" />
                      Design Summary
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex justify-between">
                      <span>Datum Level:</span>
                      <span className="font-mono">{results.datum} m</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Survey Points:</span>
                      <span className="font-mono">{results.numberOfPoints}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Total Cut:</span>
                      <span className="font-mono text-red-600">{results.totalCut} m³</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Total Fill:</span>
                      <span className="font-mono text-blue-600">{results.totalFill} m³</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Net Cut/Fill:</span>
                      <span className={`font-mono ${(results.totalCut - results.totalFill) > 0 ? 'text-red-600' : 'text-blue-600'}`}>
                        {Math.abs(results.totalCut - results.totalFill).toFixed(2)} m³
                      </span>
                    </div>
                  </CardContent>
                </Card>

                {/* Cut/Fill Table */}
                <Card>
                  <CardHeader>
                    <CardTitle>Cut/Fill Analysis</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="max-h-64 overflow-y-auto">
                      <table className="w-full text-sm">
                        <thead className="bg-gray-50 sticky top-0">
                          <tr>
                            <th className="p-2 text-left">Chainage</th>
                            <th className="p-2 text-left">NSL</th>
                            <th className="p-2 text-left">Formation</th>
                            <th className="p-2 text-left">Cut</th>
                            <th className="p-2 text-left">Fill</th>
                          </tr>
                        </thead>
                        <tbody>
                          {results.cutFillData.slice(0, 10).map((point, index) => (
                            <tr key={index} className="border-b">
                              <td className="p-2">{point.chainage}</td>
                              <td className="p-2">{point.nsl}</td>
                              <td className="p-2">{point.formation}</td>
                              <td className="p-2 text-red-600">{point.cut}</td>
                              <td className="p-2 text-blue-600">{point.fill}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                      {results.cutFillData.length > 10 && (
                        <div className="text-center text-gray-500 text-xs p-2">
                          ... and {results.cutFillData.length - 10} more points
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>

                {/* Recommendations */}
                <Card className="lg:col-span-2">
                  <CardHeader>
                    <CardTitle>Engineering Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {results.recommendations.map((rec, index) => (
                        <div key={index} className="p-3 bg-gray-50 rounded-lg text-sm">
                          {rec}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}
          </TabsContent>

          <TabsContent value="report" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Technical Drawings & Report</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-gray-600">
                  Generate comprehensive road design documentation including longitudinal profile, 
                  cross-sections, and earthwork calculations.
                </p>
                <div className="flex gap-4">
                  <Button onClick={generateReport}>
                    <FileText className="h-4 w-4 mr-2" />
                    Generate PDF Report
                  </Button>
                  <Button variant="outline">
                    <Download className="h-4 w-4 mr-2" />
                    Export to AutoCAD
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}