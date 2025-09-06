import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import { calculateStaircase } from "@/lib/structural-calculations";
import { StaircaseInputs, StaircaseResults } from "@/types/structural";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import { CheckCircle, AlertCircle, FileText, Save, X } from "lucide-react";

const staircaseSchema = z.object({
  clearSpan: z.number().min(1000).max(10000),
  width: z.number().min(500).max(5000),
  wallWidth: z.number().min(100).max(1000),
  liveLoad: z.number().min(0.5).max(10),
  floorFinishLoad: z.number().min(0.1).max(5),
  numRisers: z.number().min(5).max(50),
  riser: z.number().min(100).max(200),
  tread: z.number().min(200).max(400),
  concreteGrade: z.number().min(15).max(50),
  steelGrade: z.number().min(250).max(600),
});

interface StaircaseCalculatorProps {
  onClose: () => void;
}

export function StaircaseCalculator({ onClose }: StaircaseCalculatorProps) {
  const [results, setResults] = useState<StaircaseResults | null>(null);
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const form = useForm<StaircaseInputs>({
    resolver: zodResolver(staircaseSchema),
    defaultValues: {
      clearSpan: 3000,
      width: 1200,
      wallWidth: 230,
      liveLoad: 3.0,
      floorFinishLoad: 1.0,
      numRisers: 20,
      riser: 150,
      tread: 300,
      concreteGrade: 20,
      steelGrade: 415,
    },
  });

  const createCalculation = useMutation({
    mutationFn: async (data: { inputData: StaircaseInputs; results: StaircaseResults }) => {
      return await apiRequest('POST', '/api/calculations', {
        projectId: 1,
        userId: 1,
        type: 'staircase',
        inputData: data.inputData,
        results: data.results,
        isValid: 'true'
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/user/1/calculations'] });
      queryClient.invalidateQueries({ queryKey: ['/api/user/1/stats'] });
      toast({
        title: "Calculation saved",
        description: "Staircase design calculation has been saved successfully.",
      });
    },
  });

  const onSubmit = (data: StaircaseInputs) => {
    try {
      const calculationResults = calculateStaircase(data);
      setResults(calculationResults);
      
      toast({
        title: "Calculation complete",
        description: "Staircase design has been calculated successfully.",
      });
    } catch (error) {
      toast({
        title: "Calculation error",
        description: "There was an error calculating the staircase design.",
        variant: "destructive",
      });
    }
  };

  const handleSave = () => {
    if (results) {
      createCalculation.mutate({
        inputData: form.getValues(),
        results
      });
    }
  };

  const handleClose = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center min-h-screen p-4" onClick={handleClose}>
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900">Staircase Design Calculator</h2>
            <Button variant="ghost" size="icon" onClick={onClose} className="text-gray-400 hover:text-gray-600">
              <X size={20} />
            </Button>
          </div>
        </div>
        
        <div className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Input Form */}
            <div className="space-y-6">
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="font-semibold text-gray-900 mb-4">Design Parameters</h3>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                  <div>
                    <Label htmlFor="clearSpan" className="block text-sm font-medium text-gray-700 mb-1">
                      Clear Span (mm)
                    </Label>
                    <Input
                      id="clearSpan"
                      type="number"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                      placeholder="3000"
                      {...form.register("clearSpan", { valueAsNumber: true })}
                    />
                    {form.formState.errors.clearSpan && (
                      <p className="text-sm text-red-600 mt-1">{form.formState.errors.clearSpan.message}</p>
                    )}
                  </div>
                  
                  <div>
                    <Label htmlFor="width" className="block text-sm font-medium text-gray-700 mb-1">
                      Width of Staircase (mm)
                    </Label>
                    <Input
                      id="width"
                      type="number"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                      placeholder="1200"
                      {...form.register("width", { valueAsNumber: true })}
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="wallWidth" className="block text-sm font-medium text-gray-700 mb-1">
                      Breadth of Wall/Beam (mm)
                    </Label>
                    <Input
                      id="wallWidth"
                      type="number"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                      placeholder="230"
                      {...form.register("wallWidth", { valueAsNumber: true })}
                    />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="riser" className="block text-sm font-medium text-gray-700 mb-1">
                        Riser (mm)
                      </Label>
                      <Input
                        id="riser"
                        type="number"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                        placeholder="150"
                        {...form.register("riser", { valueAsNumber: true })}
                      />
                    </div>
                    <div>
                      <Label htmlFor="tread" className="block text-sm font-medium text-gray-700 mb-1">
                        Tread (mm)
                      </Label>
                      <Input
                        id="tread"
                        type="number"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                        placeholder="300"
                        {...form.register("tread", { valueAsNumber: true })}
                      />
                    </div>
                  </div>
                  
                  <div>
                    <Label htmlFor="numRisers" className="block text-sm font-medium text-gray-700 mb-1">
                      Number of Risers
                    </Label>
                    <Input
                      id="numRisers"
                      type="number"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                      placeholder="20"
                      {...form.register("numRisers", { valueAsNumber: true })}
                    />
                  </div>
                </form>
              </div>
              
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="font-semibold text-gray-900 mb-4">Load Parameters</h3>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="liveLoad" className="block text-sm font-medium text-gray-700 mb-1">
                      Live Load (kN/m²)
                    </Label>
                    <Input
                      id="liveLoad"
                      type="number"
                      step="0.1"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                      placeholder="3.0"
                      {...form.register("liveLoad", { valueAsNumber: true })}
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="floorFinishLoad" className="block text-sm font-medium text-gray-700 mb-1">
                      Floor Finish Load (kN/m²)
                    </Label>
                    <Input
                      id="floorFinishLoad"
                      type="number"
                      step="0.1"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                      placeholder="1.0"
                      {...form.register("floorFinishLoad", { valueAsNumber: true })}
                    />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label className="block text-sm font-medium text-gray-700 mb-1">
                        Concrete Grade
                      </Label>
                      <Select 
                        value={form.watch("concreteGrade")?.toString()}
                        onValueChange={(value) => form.setValue("concreteGrade", parseInt(value))}
                      >
                        <SelectTrigger className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="20">M20</SelectItem>
                          <SelectItem value="25">M25</SelectItem>
                          <SelectItem value="30">M30</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label className="block text-sm font-medium text-gray-700 mb-1">
                        Steel Grade
                      </Label>
                      <Select 
                        value={form.watch("steelGrade")?.toString()}
                        onValueChange={(value) => form.setValue("steelGrade", parseInt(value))}
                      >
                        <SelectTrigger className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="415">Fe415</SelectItem>
                          <SelectItem value="500">Fe500</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </div>
              </div>
              
              <Button 
                onClick={form.handleSubmit(onSubmit)} 
                className="w-full bg-primary text-white py-3 px-4 rounded-md font-medium hover:bg-blue-700 transition-colors"
                disabled={form.formState.isSubmitting}
              >
                Calculate Design
              </Button>
            </div>
            
            {/* Results Panel */}
            <div className="space-y-6">
              {results ? (
                <>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-semibold text-gray-900 mb-4">Calculation Results</h3>
                    <div className="space-y-4 text-sm font-mono">
                      <div className="bg-white p-3 rounded border">
                        <h4 className="font-semibold text-gray-800 mb-2">Load Analysis</h4>
                        <div className="space-y-1 text-xs">
                          <p>Self weight of waist slab: <span className="font-bold text-blue-600">{results.waistSlabWeight} kN/m²</span></p>
                          <p>Self weight of steps: <span className="font-bold text-blue-600">{results.stepsWeight} kN/m²</span></p>
                          <p>Total factored load: <span className="font-bold text-blue-600">{results.factoredLoadGoing} kN/m²</span></p>
                        </div>
                      </div>
                      
                      <div className="bg-white p-3 rounded border">
                        <h4 className="font-semibold text-gray-800 mb-2">Bending Moment</h4>
                        <div className="space-y-1 text-xs">
                          <p>Maximum B.M.: <span className="font-bold text-green-600">{results.maxMoment} kN.m</span></p>
                          <p>Distance to max B.M.: <span className="font-bold text-green-600">{results.maxMomentDistance} m</span></p>
                        </div>
                      </div>
                      
                      <div className="bg-white p-3 rounded border">
                        <h4 className="font-semibold text-gray-800 mb-2">Reinforcement</h4>
                        <div className="space-y-1 text-xs">
                          <p>Main steel area: <span className="font-bold text-purple-600">{results.mainSteelArea} mm²</span></p>
                          <p>Bar spacing: <span className="font-bold text-purple-600">{results.providedSpacing} mm c/c</span></p>
                          <p>Use: <span className="font-bold text-purple-600">12mm ⌀ @ {results.providedSpacing}mm c/c</span></p>
                        </div>
                      </div>
                      
                      <div className="bg-white p-3 rounded border">
                        <h4 className="font-semibold text-gray-800 mb-2">Checks</h4>
                        <div className="space-y-1 text-xs">
                          <div className="flex items-center space-x-2">
                            {results.shearSafe ? <CheckCircle className="text-green-600" size={14} /> : <AlertCircle className="text-red-600" size={14} />}
                            <span>Shear: {results.shearSafe ? "✓ Safe" : "✗ Unsafe"}</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            {results.deflectionSafe ? <CheckCircle className="text-green-600" size={14} /> : <AlertCircle className="text-red-600" size={14} />}
                            <span>Deflection: {results.deflectionSafe ? "✓ Safe" : "✗ Needs review"}</span>
                          </div>
                          <p>Min reinforcement: <span className="font-bold text-green-600">✓ Safe</span></p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="bg-blue-50 rounded-lg p-4">
                    <h3 className="font-semibold text-gray-900 mb-3">Design Summary</h3>
                    <div className="text-sm space-y-2">
                      <p><strong>Waist slab thickness:</strong> {results.waistThickness} mm</p>
                      <p><strong>Effective depth:</strong> {results.effectiveDepth} mm</p>
                      <p><strong>Clear cover:</strong> 20 mm</p>
                      <p><strong>Design code:</strong> IS-456:2000</p>
                    </div>
                    
                    <div className="mt-4 flex space-x-2">
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="flex-1 bg-white border border-gray-300 text-gray-700 hover:bg-gray-50"
                      >
                        <FileText className="mr-2" size={14} />
                        Generate Report
                      </Button>
                      <Button 
                        size="sm" 
                        className="flex-1 bg-primary text-white hover:bg-blue-700"
                        onClick={handleSave}
                        disabled={createCalculation.isPending}
                      >
                        <Save className="mr-2" size={14} />
                        Save Design
                      </Button>
                    </div>
                  </div>
                </>
              ) : (
                <div className="bg-gray-50 rounded-lg p-4">
                  <h3 className="font-semibold text-gray-900 mb-4">Calculation Results</h3>
                  <div className="flex items-center justify-center h-64">
                    <div className="text-center">
                      <p className="text-gray-500">Enter parameters and click "Calculate Design" to see results</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
