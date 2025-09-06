import { useState, useRef, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { 
  Ruler, 
  Calculator, 
  Download, 
  RotateCcw, 
  Eye,
  EyeOff,
  Settings,
  FileText,
  Share2
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface BeamParameters {
  webWidth: number;
  totalDepth: number;
  topFlangeThickness: number;
  bottomFlangeThickness: number;
  bottomBarDiameter: number;
  numberOfBottomBars: number;
  topBarDiameter: number;
  numberOfTopBars: number;
  stirrupDiameter: number;
  stirrupSpacing: number;
  scale: number;
  beamNumber: string;
}

interface BeamDrawing {
  width: number;
  height: number;
  scale: number;
  showDimensions: boolean;
  showReinforcement: boolean;
  showStirrups: boolean;
}

export default function BeamDesign() {
  const [searchParams] = useSearchParams();
  const beamType = searchParams.get("type") || "l-beam";
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  const [parameters, setParameters] = useState<BeamParameters>({
    webWidth: 300,
    totalDepth: 600,
    topFlangeThickness: 150,
    bottomFlangeThickness: 150,
    bottomBarDiameter: 20,
    numberOfBottomBars: 4,
    topBarDiameter: 16,
    numberOfTopBars: 2,
    stirrupDiameter: 8,
    stirrupSpacing: 150,
    scale: 50,
    beamNumber: "B-001"
  });

  const [drawing, setDrawing] = useState<BeamDrawing>({
    width: 800,
    height: 600,
    scale: 50,
    showDimensions: true,
    showReinforcement: true,
    showStirrups: true
  });

  const [activeTab, setActiveTab] = useState("design");

  // Update drawing when parameters change
  useEffect(() => {
    drawBeam();
  }, [parameters, drawing]);

  const drawBeam = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Set drawing scale
    const scale = drawing.scale / 1000; // Convert mm to meters
    const offsetX = 100;
    const offsetY = 100;

    // Draw beam outline
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    if (beamType === "l-beam") {
      // L-Beam outline
      ctx.beginPath();
      ctx.moveTo(offsetX, offsetY);
      ctx.lineTo(offsetX + parameters.webWidth * scale, offsetY);
      ctx.lineTo(offsetX + parameters.webWidth * scale, offsetY + parameters.totalDepth * scale);
      ctx.lineTo(offsetX, offsetY + parameters.totalDepth * scale);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Top flange
      ctx.beginPath();
      ctx.moveTo(offsetX, offsetY);
      ctx.lineTo(offsetX + parameters.webWidth * scale, offsetY);
      ctx.lineTo(offsetX + parameters.webWidth * scale, offsetY + parameters.topFlangeThickness * scale);
      ctx.lineTo(offsetX, offsetY + parameters.topFlangeThickness * scale);
      ctx.closePath();
      ctx.fillStyle = "#e5e7eb";
      ctx.fill();
      ctx.stroke();
    } else if (beamType === "t-beam") {
      // T-Beam outline
      ctx.beginPath();
      ctx.moveTo(offsetX, offsetY);
      ctx.lineTo(offsetX + parameters.webWidth * scale, offsetY);
      ctx.lineTo(offsetX + parameters.webWidth * scale, offsetY + parameters.topFlangeThickness * scale);
      ctx.lineTo(offsetX + (parameters.webWidth - parameters.bottomFlangeThickness) * scale, offsetY + parameters.topFlangeThickness * scale);
      ctx.lineTo(offsetX + (parameters.webWidth - parameters.bottomFlangeThickness) * scale, offsetY + parameters.totalDepth * scale);
      ctx.lineTo(offsetX, offsetY + parameters.totalDepth * scale);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    } else {
      // Rectangular beam
      ctx.beginPath();
      ctx.rect(offsetX, offsetY, parameters.webWidth * scale, parameters.totalDepth * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw reinforcement if enabled
    if (drawing.showReinforcement) {
      drawReinforcement(ctx, offsetX, offsetY, scale);
    }

    // Draw stirrups if enabled
    if (drawing.showStirrups) {
      drawStirrups(ctx, offsetX, offsetY, scale);
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawReinforcement = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#dc2626";
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 1;

    // Bottom bars
    const bottomBarSpacing = (parameters.webWidth - 50) / (parameters.numberOfBottomBars - 1);
    for (let i = 0; i < parameters.numberOfBottomBars; i++) {
      const x = offsetX + 25 + i * bottomBarSpacing;
      const y = offsetY + 25;
      ctx.beginPath();
      ctx.arc(x, y, parameters.bottomBarDiameter * scale / 2, 0, 2 * Math.PI);
      ctx.fill();
    }

    // Top bars
    const topBarSpacing = (parameters.webWidth - 50) / (parameters.numberOfTopBars - 1);
    for (let i = 0; i < parameters.numberOfTopBars; i++) {
      const x = offsetX + 25 + i * topBarSpacing;
      const y = offsetY + parameters.totalDepth * scale - 25;
      ctx.beginPath();
      ctx.arc(x, y, parameters.topBarDiameter * scale / 2, 0, 2 * Math.PI);
      ctx.fill();
    }
  };

  const drawStirrups = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#059669";
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 5]);

    const stirrupWidth = parameters.webWidth - 50;
    const stirrupHeight = parameters.totalDepth - 50;
    const numberOfStirrups = Math.floor(parameters.totalDepth / parameters.stirrupSpacing);

    for (let i = 0; i <= numberOfStirrups; i++) {
      const y = offsetY + 25 + i * parameters.stirrupSpacing * scale;
      ctx.beginPath();
      ctx.rect(offsetX + 25, y, stirrupWidth * scale, stirrupHeight * scale);
      ctx.stroke();
    }

    ctx.setLineDash([]);
  };

  const drawDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Width dimension
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY - 20);
    ctx.lineTo(offsetX + parameters.webWidth * scale, offsetY - 20);
    ctx.stroke();
    ctx.fillText(`${parameters.webWidth} mm`, offsetX + (parameters.webWidth * scale) / 2, offsetY - 25);

    // Height dimension
    ctx.beginPath();
    ctx.moveTo(offsetX - 20, offsetY);
    ctx.lineTo(offsetX - 20, offsetY + parameters.totalDepth * scale);
    ctx.stroke();
    ctx.save();
    ctx.translate(offsetX - 25, offsetY + (parameters.totalDepth * scale) / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(`${parameters.totalDepth} mm`, 0, 0);
    ctx.restore();
  };

  const handleParameterChange = (key: keyof BeamParameters, value: number | string) => {
    setParameters(prev => ({ ...prev, [key]: value }));
  };

  const resetParameters = () => {
    setParameters({
      webWidth: 300,
      totalDepth: 600,
      topFlangeThickness: 150,
      bottomFlangeThickness: 150,
      bottomBarDiameter: 20,
      numberOfBottomBars: 4,
      topBarDiameter: 16,
      numberOfTopBars: 2,
      stirrupDiameter: 8,
      stirrupSpacing: 150,
      scale: 50,
      beamNumber: "B-001"
    });
  };

  const exportDrawing = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const link = document.createElement("a");
    link.download = `beam-design-${parameters.beamNumber}.png`;
    link.href = canvas.toDataURL();
    link.click();
  };

  const getBeamTypeTitle = () => {
    switch (beamType) {
      case "l-beam": return "L-Beam Design";
      case "t-beam": return "T-Beam Design";
      case "rect-beam": return "Rectangular Beam Design";
      default: return "Beam Design";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{getBeamTypeTitle()}</h1>
          <p className="text-muted-foreground">
            Design and visualize reinforced concrete beams with real-time calculations
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={resetParameters}>
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
          <Button variant="outline" onClick={exportDrawing}>
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
          <Button>
            <Share2 className="w-4 h-4 mr-2" />
            Share Design
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="design">Design Parameters</TabsTrigger>
          <TabsTrigger value="visualization">Visualization</TabsTrigger>
          <TabsTrigger value="calculations">Calculations</TabsTrigger>
        </TabsList>

        <TabsContent value="design" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Input Parameters */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Ruler className="w-5 h-5" />
                  <span>Beam Dimensions</span>
                </CardTitle>
                <CardDescription>
                  Enter the geometric parameters for your beam design
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="webWidth">Web Width (mm)</Label>
                    <Input
                      id="webWidth"
                      type="number"
                      value={parameters.webWidth}
                      onChange={(e) => handleParameterChange("webWidth", Number(e.target.value))}
                      min="100"
                      max="1000"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="totalDepth">Total Depth (mm)</Label>
                    <Input
                      id="totalDepth"
                      type="number"
                      value={parameters.totalDepth}
                      onChange={(e) => handleParameterChange("totalDepth", Number(e.target.value))}
                      min="200"
                      max="1200"
                    />
                  </div>
                </div>

                {(beamType === "l-beam" || beamType === "t-beam") && (
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="topFlangeThickness">Top Flange (mm)</Label>
                      <Input
                        id="topFlangeThickness"
                        type="number"
                        value={parameters.topFlangeThickness}
                        onChange={(e) => handleParameterChange("topFlangeThickness", Number(e.target.value))}
                        min="50"
                        max="300"
                      />
                    </div>
                    {beamType === "t-beam" && (
                      <div className="space-y-2">
                        <Label htmlFor="bottomFlangeThickness">Bottom Flange (mm)</Label>
                        <Input
                          id="bottomFlangeThickness"
                          type="number"
                          value={parameters.bottomFlangeThickness}
                          onChange={(e) => handleParameterChange("bottomFlangeThickness", Number(e.target.value))}
                          min="50"
                          max="300"
                        />
                      </div>
                    )}
                  </div>
                )}

                <Separator />

                <div className="space-y-2">
                  <Label htmlFor="scale">Drawing Scale (1:)</Label>
                  <Slider
                    value={[parameters.scale]}
                    onValueChange={([value]) => handleParameterChange("scale", value)}
                    min={10}
                    max={100}
                    step={10}
                    className="w-full"
                  />
                  <div className="text-sm text-muted-foreground">
                    Current scale: 1:{parameters.scale}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Reinforcement Parameters */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Calculator className="w-5 h-5" />
                  <span>Reinforcement Details</span>
                </CardTitle>
                <CardDescription>
                  Configure reinforcement bars and stirrups
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="bottomBarDiameter">Bottom Bar Diameter (mm)</Label>
                    <Select
                      value={parameters.bottomBarDiameter.toString()}
                      onValueChange={(value) => handleParameterChange("bottomBarDiameter", Number(value))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {[12, 16, 20, 25, 32, 40].map((diameter) => (
                          <SelectItem key={diameter} value={diameter.toString()}>
                            {diameter} mm
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="numberOfBottomBars">Number of Bottom Bars</Label>
                    <Input
                      id="numberOfBottomBars"
                      type="number"
                      value={parameters.numberOfBottomBars}
                      onChange={(e) => handleParameterChange("numberOfBottomBars", Number(e.target.value))}
                      min="2"
                      max="8"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="topBarDiameter">Top Bar Diameter (mm)</Label>
                    <Select
                      value={parameters.topBarDiameter.toString()}
                      onValueChange={(value) => handleParameterChange("topBarDiameter", Number(value))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {[12, 16, 20, 25, 32].map((diameter) => (
                          <SelectItem key={diameter} value={diameter.toString()}>
                            {diameter} mm
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="numberOfTopBars">Number of Top Bars</Label>
                    <Input
                      id="numberOfTopBars"
                      type="number"
                      value={parameters.numberOfTopBars}
                      onChange={(e) => handleParameterChange("numberOfTopBars", Number(e.target.value))}
                      min="2"
                      max="6"
                    />
                  </div>
                </div>

                <Separator />

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="stirrupDiameter">Stirrup Diameter (mm)</Label>
                    <Select
                      value={parameters.stirrupDiameter.toString()}
                      onValueChange={(value) => handleParameterChange("stirrupDiameter", Number(value))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {[6, 8, 10, 12].map((diameter) => (
                          <SelectItem key={diameter} value={diameter.toString()}>
                            {diameter} mm
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="stirrupSpacing">Stirrup Spacing (mm)</Label>
                    <Input
                      id="stirrupSpacing"
                      type="number"
                      value={parameters.stirrupSpacing}
                      onChange={(e) => handleParameterChange("stirrupSpacing", Number(e.target.value))}
                      min="100"
                      max="300"
                      step="25"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="beamNumber">Beam Number</Label>
                  <Input
                    id="beamNumber"
                    value={parameters.beamNumber}
                    onChange={(e) => handleParameterChange("beamNumber", e.target.value)}
                    placeholder="B-001"
                  />
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="visualization" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Eye className="w-5 h-5" />
                <span>Beam Visualization</span>
              </CardTitle>
              <CardDescription>
                Real-time 2D representation of your beam design
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Visualization Controls */}
                <div className="flex items-center space-x-6">
                  <div className="flex items-center space-x-2">
                    <Switch
                      id="showDimensions"
                      checked={drawing.showDimensions}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showDimensions: checked }))}
                    />
                    <Label htmlFor="showDimensions">Show Dimensions</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Switch
                      id="showReinforcement"
                      checked={drawing.showReinforcement}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showReinforcement: checked }))}
                    />
                    <Label htmlFor="showReinforcement">Show Reinforcement</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Switch
                      id="showStirrups"
                      checked={drawing.showStirrups}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showStirrups: checked }))}
                    />
                    <Label htmlFor="showStirrups">Show Stirrups</Label>
                  </div>
                </div>

                {/* Canvas */}
                <div className="border rounded-lg p-4 bg-gray-50">
                  <canvas
                    ref={canvasRef}
                    width={drawing.width}
                    height={drawing.height}
                    className="border border-gray-300 rounded bg-white mx-auto block"
                  />
                </div>

                {/* Drawing Info */}
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div className="text-center">
                    <div className="font-medium">Scale</div>
                    <div className="text-muted-foreground">1:{parameters.scale}</div>
                  </div>
                  <div className="text-center">
                    <div className="font-medium">Canvas Size</div>
                    <div className="text-muted-foreground">{drawing.width} × {drawing.height} px</div>
                  </div>
                  <div className="text-center">
                    <div className="font-medium">Beam Number</div>
                    <div className="text-muted-foreground">{parameters.beamNumber}</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="calculations" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Calculator className="w-5 h-5" />
                <span>Design Calculations</span>
              </CardTitle>
              <CardDescription>
                Structural analysis and reinforcement calculations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {/* Cross-sectional Properties */}
                <div>
                  <h4 className="font-semibold mb-3">Cross-sectional Properties</h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-50 p-3 rounded">
                      <div className="text-sm text-muted-foreground">Gross Area</div>
                      <div className="text-lg font-semibold">
                        {((parameters.webWidth * parameters.totalDepth) / 1000000).toFixed(3)} m²
                      </div>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <div className="text-sm text-muted-foreground">Perimeter</div>
                      <div className="text-lg font-semibold">
                        {((2 * (parameters.webWidth + parameters.totalDepth)) / 1000).toFixed(2)} m
                      </div>
                    </div>
                  </div>
                </div>

                {/* Reinforcement Summary */}
                <div>
                  <h4 className="font-semibold mb-3">Reinforcement Summary</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center p-3 bg-blue-50 rounded">
                      <span>Bottom Reinforcement</span>
                      <Badge variant="secondary">
                        {parameters.numberOfBottomBars} nos. {parameters.bottomBarDiameter}φ
                      </Badge>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-green-50 rounded">
                      <span>Top Reinforcement</span>
                      <Badge variant="secondary">
                        {parameters.numberOfTopBars} nos. {parameters.topBarDiameter}φ
                      </Badge>
                    </div>
                    <div className="flex justify-between items-center p-3 bg-yellow-50 rounded">
                      <span>Stirrups</span>
                      <Badge variant="secondary">
                        {parameters.stirrupDiameter}φ @ {parameters.stirrupSpacing} mm c/c
                      </Badge>
                    </div>
                  </div>
                </div>

                {/* Design Notes */}
                <div>
                  <h4 className="font-semibold mb-3">Design Notes</h4>
                  <div className="bg-gray-50 p-4 rounded space-y-2 text-sm">
                    <div>• Beam designed according to IS-456:2000</div>
                    <div>• Clear cover: 25 mm on all sides</div>
                    <div>• Minimum reinforcement: 0.85% of gross area</div>
                    <div>• Maximum reinforcement: 4% of gross area</div>
                    <div>• Stirrup spacing should not exceed 0.75d</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
