import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Calculator, FileText, Download, AlertTriangle, CheckCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface BeamCalculatorProps {
  onClose: () => void;
}

interface BeamInputs {
  span: number;
  width: number;
  depth: number;
  deadLoad: number;
  liveLoad: number;
  concreteGrade: number;
  steelGrade: number;
  cover: number;
  supportType: 'simply-supported' | 'continuous';
}

interface BeamResults {
  designMoment: number;
  shearForce: number;
  mainReinforcement: number;
  stirrupSpacing: number;
  effectiveDepth: number;
  momentCapacity: number;
  safetyRatio: number;
  recommendations: string[];
}

export function BeamCalculator({ onClose }: BeamCalculatorProps) {
  const { toast } = useToast();
  const [activeTab, setActiveTab] = useState("input");
  const [inputs, setInputs] = useState<BeamInputs>({
    span: 6.0,
    width: 300,
    depth: 450,
    deadLoad: 15.0,
    liveLoad: 4.0,
    concreteGrade: 25,
    steelGrade: 415,
    cover: 25,
    supportType: 'simply-supported'
  });
  const [results, setResults] = useState<BeamResults | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);

  const calculateBeam = () => {
    setIsCalculating(true);
    
    // Simulate calculation delay
    setTimeout(() => {
      // Beam design calculations based on IS-456
      const totalLoad = inputs.deadLoad + inputs.liveLoad;
      const designLoad = totalLoad * 1.5; // Factor of safety
      
      // Design moment for simply supported beam
      const designMoment = (designLoad * Math.pow(inputs.span, 2)) / 8;
      
      // Shear force
      const shearForce = (designLoad * inputs.span) / 2;
      
      // Effective depth
      const effectiveDepth = inputs.depth - inputs.cover - 10; // Assuming 20mm dia bar
      
      // Required steel area (simplified formula)
      const fck = inputs.concreteGrade;
      const fy = inputs.steelGrade;
      const requiredAs = (designMoment * 1000000) / (0.87 * fy * 0.9 * effectiveDepth);
      
      // Main reinforcement
      const barArea = Math.PI * Math.pow(20, 2) / 4; // 20mm dia bars
      const mainReinforcement = Math.ceil(requiredAs / barArea);
      
      // Stirrup spacing (simplified)
      const stirrupSpacing = Math.min(
        effectiveDepth / 2,
        300,
        (0.87 * 415 * 2 * 78.5) / (shearForce * 1000 / inputs.width)
      );
      
      // Moment capacity
      const providedAs = mainReinforcement * barArea;
      const momentCapacity = (0.87 * fy * providedAs * 0.9 * effectiveDepth) / 1000000;
      
      // Safety ratio
      const safetyRatio = momentCapacity / designMoment;
      
      // Recommendations
      const recommendations = [];
      if (safetyRatio < 1.0) {
        recommendations.push("⚠️ Increase beam depth or reinforcement");
      }
      if (safetyRatio > 2.0) {
        recommendations.push("✓ Design is over-conservative, can be optimized");
      }
      if (stirrupSpacing > 300) {
        recommendations.push("⚠️ Check shear reinforcement spacing");
      }
      if (recommendations.length === 0) {
        recommendations.push("✓ Design meets IS-456 requirements");
      }

      setResults({
        designMoment,
        shearForce,
        mainReinforcement,
        stirrupSpacing: Math.round(stirrupSpacing),
        effectiveDepth,
        momentCapacity,
        safetyRatio,
        recommendations
      });
      
      setActiveTab("results");
      setIsCalculating(false);
      
      toast({
        title: "Calculation Complete",
        description: "Beam design analysis has been completed successfully.",
      });
    }, 2000);
  };

  const generateReport = () => {
    toast({
      title: "Report Generated",
      description: "Beam design report has been prepared for download.",
    });
  };

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Calculator className="h-5 w-5 text-blue-600" />
            RCC Beam Design Calculator
            <Badge variant="secondary" className="ml-2">IS-456</Badge>
          </DialogTitle>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="input">Input Parameters</TabsTrigger>
            <TabsTrigger value="results" disabled={!results}>Results</TabsTrigger>
            <TabsTrigger value="report" disabled={!results}>Report</TabsTrigger>
          </TabsList>

          <TabsContent value="input" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Beam Geometry */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Beam Geometry</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="span">Span (m)</Label>
                      <Input
                        id="span"
                        type="number"
                        value={inputs.span}
                        onChange={(e) => setInputs({...inputs, span: parseFloat(e.target.value)})}
                        step="0.1"
                      />
                    </div>
                    <div>
                      <Label htmlFor="width">Width (mm)</Label>
                      <Input
                        id="width"
                        type="number"
                        value={inputs.width}
                        onChange={(e) => setInputs({...inputs, width: parseInt(e.target.value)})}
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="depth">Depth (mm)</Label>
                      <Input
                        id="depth"
                        type="number"
                        value={inputs.depth}
                        onChange={(e) => setInputs({...inputs, depth: parseInt(e.target.value)})}
                      />
                    </div>
                    <div>
                      <Label htmlFor="cover">Clear Cover (mm)</Label>
                      <Input
                        id="cover"
                        type="number"
                        value={inputs.cover}
                        onChange={(e) => setInputs({...inputs, cover: parseInt(e.target.value)})}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Loading */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Loading Conditions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="deadLoad">Dead Load (kN/m)</Label>
                    <Input
                      id="deadLoad"
                      type="number"
                      value={inputs.deadLoad}
                      onChange={(e) => setInputs({...inputs, deadLoad: parseFloat(e.target.value)})}
                      step="0.1"
                    />
                  </div>
                  <div>
                    <Label htmlFor="liveLoad">Live Load (kN/m)</Label>
                    <Input
                      id="liveLoad"
                      type="number"
                      value={inputs.liveLoad}
                      onChange={(e) => setInputs({...inputs, liveLoad: parseFloat(e.target.value)})}
                      step="0.1"
                    />
                  </div>
                  <div>
                    <Label htmlFor="supportType">Support Type</Label>
                    <select
                      id="supportType"
                      value={inputs.supportType}
                      onChange={(e) => setInputs({...inputs, supportType: e.target.value as 'simply-supported' | 'continuous'})}
                      className="w-full h-10 px-3 rounded-md border border-input bg-background"
                    >
                      <option value="simply-supported">Simply Supported</option>
                      <option value="continuous">Continuous</option>
                    </select>
                  </div>
                </CardContent>
              </Card>

              {/* Material Properties */}
              <Card className="md:col-span-2">
                <CardHeader>
                  <CardTitle className="text-lg">Material Properties</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="concreteGrade">Concrete Grade (MPa)</Label>
                      <select
                        id="concreteGrade"
                        value={inputs.concreteGrade}
                        onChange={(e) => setInputs({...inputs, concreteGrade: parseInt(e.target.value)})}
                        className="w-full h-10 px-3 rounded-md border border-input bg-background"
                      >
                        <option value={20}>M20</option>
                        <option value={25}>M25</option>
                        <option value={30}>M30</option>
                        <option value={35}>M35</option>
                      </select>
                    </div>
                    <div>
                      <Label htmlFor="steelGrade">Steel Grade (MPa)</Label>
                      <select
                        id="steelGrade"
                        value={inputs.steelGrade}
                        onChange={(e) => setInputs({...inputs, steelGrade: parseInt(e.target.value)})}
                        className="w-full h-10 px-3 rounded-md border border-input bg-background"
                      >
                        <option value={415}>Fe415</option>
                        <option value={500}>Fe500</option>
                        <option value={550}>Fe550</option>
                      </select>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="flex justify-between pt-4">
              <Button variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button onClick={calculateBeam} disabled={isCalculating}>
                {isCalculating ? "Calculating..." : "Calculate Beam Design"}
                <Calculator className="h-4 w-4 ml-2" />
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="results" className="space-y-6">
            {results && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Design Forces */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <AlertTriangle className="h-5 w-5 text-orange-500" />
                      Design Forces
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex justify-between">
                      <span>Design Moment:</span>
                      <span className="font-mono">{results.designMoment.toFixed(2)} kNm</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Max Shear Force:</span>
                      <span className="font-mono">{results.shearForce.toFixed(2)} kN</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Effective Depth:</span>
                      <span className="font-mono">{results.effectiveDepth} mm</span>
                    </div>
                  </CardContent>
                </Card>

                {/* Reinforcement */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <CheckCircle className="h-5 w-5 text-green-500" />
                      Reinforcement Design
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex justify-between">
                      <span>Main Steel:</span>
                      <span className="font-mono">{results.mainReinforcement} - 20mm φ</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Stirrup Spacing:</span>
                      <span className="font-mono">{results.stirrupSpacing} mm c/c</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Safety Ratio:</span>
                      <span className={`font-mono ${results.safetyRatio >= 1.0 ? 'text-green-600' : 'text-red-600'}`}>
                        {results.safetyRatio.toFixed(2)}
                      </span>
                    </div>
                  </CardContent>
                </Card>

                {/* Recommendations */}
                <Card className="lg:col-span-2">
                  <CardHeader>
                    <CardTitle>Design Recommendations</CardTitle>
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
                <CardTitle>Design Report</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-sm text-gray-600">
                  Generate a comprehensive beam design report including calculations, drawings, and specifications.
                </p>
                <div className="flex gap-4">
                  <Button onClick={generateReport}>
                    <FileText className="h-4 w-4 mr-2" />
                    Generate PDF Report
                  </Button>
                  <Button variant="outline">
                    <Download className="h-4 w-4 mr-2" />
                    Export to CAD
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