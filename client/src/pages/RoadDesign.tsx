import { useState, useRef, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Road,
  Download,
  RotateCcw,
  Eye,
  Share2,
  Ruler,
  Map
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface RoadParameters {
  length: number;
  interval: number;
  naturalGroundLevel: number;
  formationLevel: number;
  roadWidth: number;
  shoulderWidth: number;
  scale: number;
  roadNumber: string;
}

interface RoadDrawing {
  width: number;
  height: number;
  scale: number;
  showDimensions: boolean;
  showGrid: boolean;
  showLevels: boolean;
  showCrossSection: boolean;
}

export default function RoadDesign() {
  const [searchParams] = useSearchParams();
  const roadType = searchParams.get("type") || "l-section";
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [parameters, setParameters] = useState<RoadParameters>({
    length: 1000,
    interval: 50,
    naturalGroundLevel: 100,
    formationLevel: 98,
    roadWidth: 7000,
    shoulderWidth: 1500,
    scale: 50,
    roadNumber: "R-001"
  });

  const [drawing, setDrawing] = useState<RoadDrawing>({
    width: 1000,
    height: 600,
    scale: 50,
    showDimensions: true,
    showGrid: false,
    showLevels: true,
    showCrossSection: true
  });

  const [activeTab, setActiveTab] = useState("drawing");

  // Update drawing when parameters change
  useEffect(() => {
    drawRoad();
  }, [parameters, drawing]);

  const drawRoad = () => {
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

    if (roadType === "l-section") {
      drawLongitudinalSection(ctx, offsetX, offsetY, scale);
    } else if (roadType === "cross-section") {
      drawCrossSection(ctx, offsetX, offsetY, scale);
    } else if (roadType === "plan") {
      drawRoadPlan(ctx, offsetX, offsetY, scale);
    } else if (roadType === "pmgsy") {
      drawPMGSYRoad(ctx, offsetX, offsetY, scale);
    }

    // Draw grid if enabled
    if (drawing.showGrid) {
      drawGrid(ctx, offsetX, offsetY, scale);
    }
  };

  const drawLongitudinalSection = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw road length
    const roadLength = parameters.length * scale;
    const roadHeight = 50;

    // Draw road surface
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, roadLength, roadHeight);
    ctx.fill();
    ctx.stroke();

    // Draw natural ground level
    ctx.strokeStyle = "#059669";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY + 150);
    
    const intervals = Math.floor(parameters.length / parameters.interval);
    for (let i = 0; i <= intervals; i++) {
      const x = offsetX + i * parameters.interval * scale;
      const y = offsetY + 150 - (parameters.naturalGroundLevel - 100) * 0.5;
      ctx.lineTo(x, y);
    }
    ctx.stroke();

    // Draw formation level
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY + 200);
    ctx.lineTo(offsetX + roadLength, offsetY + 200);
    ctx.stroke();

    // Draw levels if enabled
    if (drawing.showLevels) {
      drawLevels(ctx, offsetX, offsetY, scale);
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawLongitudinalDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawCrossSection = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    const centerX = offsetX + 400;
    const centerY = offsetY + 300;
    const roadHalfWidth = (parameters.roadWidth * scale) / 2;
    const shoulderWidth = parameters.shoulderWidth * scale;

    // Draw road surface
    ctx.beginPath();
    ctx.rect(centerX - roadHalfWidth, centerY - 20, parameters.roadWidth * scale, 40);
    ctx.fill();
    ctx.stroke();

    // Draw shoulders
    ctx.fillStyle = "#e5e7eb";
    ctx.beginPath();
    ctx.rect(centerX - roadHalfWidth - shoulderWidth, centerY - 15, shoulderWidth, 30);
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.rect(centerX + roadHalfWidth, centerY - 15, shoulderWidth, 30);
    ctx.fill();
    ctx.stroke();

    // Draw center line
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 2;
    ctx.setLineDash([10, 5]);
    ctx.beginPath();
    ctx.moveTo(centerX, centerY - 20);
    ctx.lineTo(centerX, centerY + 20);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawCrossSectionDimensions(ctx, centerX, centerY, scale);
    }
  };

  const drawRoadPlan = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    const roadLength = parameters.length * scale;
    const roadWidth = parameters.roadWidth * scale;

    // Draw road plan
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 100, roadLength, roadWidth);
    ctx.fill();
    ctx.stroke();

    // Draw center line
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 2;
    ctx.setLineDash([10, 5]);
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY + 100 + roadWidth / 2);
    ctx.lineTo(offsetX + roadLength, offsetY + 100 + roadWidth / 2);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw intervals
    const intervals = Math.floor(parameters.length / parameters.interval);
    ctx.strokeStyle = "#6b7280";
    ctx.lineWidth = 1;
    for (let i = 1; i < intervals; i++) {
      const x = offsetX + i * parameters.interval * scale;
      ctx.beginPath();
      ctx.moveTo(x, offsetY + 100);
      ctx.lineTo(x, offsetY + 100 + roadWidth);
      ctx.stroke();
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawPlanDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawPMGSYRoad = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    const roadLength = parameters.length * scale;
    const roadWidth = 3500 * scale; // PMGSY standard width

    // Draw PMGSY road
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 150, roadLength, roadWidth);
    ctx.fill();
    ctx.stroke();

    // Draw center line
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 2;
    ctx.setLineDash([10, 5]);
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY + 150 + roadWidth / 2);
    ctx.lineTo(offsetX + roadLength, offsetY + 150 + roadWidth / 2);
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw edge lines
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY + 150);
    ctx.lineTo(offsetX + roadLength, offsetY + 150);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY + 150 + roadWidth);
    ctx.lineTo(offsetX + roadLength, offsetY + 150 + roadWidth);
    ctx.stroke();

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawPMGSYDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawLevels = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "left";

    // Natural Ground Level
    ctx.fillText(`NGL: ${parameters.naturalGroundLevel} m`, offsetX + 10, offsetY + 140);
    
    // Formation Level
    ctx.fillText(`FL: ${parameters.formationLevel} m`, offsetX + 10, offsetY + 220);
  };

  const drawLongitudinalDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Length dimension
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY + 280);
    ctx.lineTo(offsetX + parameters.length * scale, offsetY + 280);
    ctx.stroke();
    ctx.fillText(`${parameters.length} m`, offsetX + (parameters.length * scale) / 2, offsetY + 295);

    // Interval markers
    const intervals = Math.floor(parameters.length / parameters.interval);
    for (let i = 0; i <= intervals; i++) {
      const x = offsetX + i * parameters.interval * scale;
      ctx.beginPath();
      ctx.moveTo(x, offsetY + 275);
      ctx.lineTo(x, offsetY + 285);
      ctx.stroke();
      if (i > 0 && i < intervals) {
        ctx.fillText(`${i * parameters.interval}`, x, offsetY + 300);
      }
    }
  };

  const drawCrossSectionDimensions = (ctx: CanvasRenderingContext2D, centerX: number, centerY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Road width
    ctx.beginPath();
    ctx.moveTo(centerX - (parameters.roadWidth * scale) / 2, centerY - 40);
    ctx.lineTo(centerX + (parameters.roadWidth * scale) / 2, centerY - 40);
    ctx.stroke();
    ctx.fillText(`${parameters.roadWidth} mm`, centerX, centerY - 50);

    // Shoulder width
    ctx.beginPath();
    ctx.moveTo(centerX - (parameters.roadWidth * scale) / 2 - parameters.shoulderWidth * scale, centerY - 40);
    ctx.lineTo(centerX - (parameters.roadWidth * scale) / 2, centerY - 40);
    ctx.stroke();
    ctx.fillText(`${parameters.shoulderWidth} mm`, centerX - (parameters.roadWidth * scale) / 4, centerY - 50);
  };

  const drawPlanDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Road length
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY + 80);
    ctx.lineTo(offsetX + parameters.length * scale, offsetY + 80);
    ctx.stroke();
    ctx.fillText(`${parameters.length} m`, offsetX + (parameters.length * scale) / 2, offsetY + 70);

    // Road width
    ctx.beginPath();
    ctx.moveTo(offsetX - 20, offsetY + 100);
    ctx.lineTo(offsetX - 20, offsetY + 100 + parameters.roadWidth * scale);
    ctx.stroke();
    ctx.save();
    ctx.translate(offsetX - 25, offsetY + 100 + (parameters.roadWidth * scale) / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(`${parameters.roadWidth} mm`, 0, 0);
    ctx.restore();
  };

  const drawPMGSYDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Road length
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY + 130);
    ctx.lineTo(offsetX + parameters.length * scale, offsetY + 130);
    ctx.stroke();
    ctx.fillText(`${parameters.length} m`, offsetX + (parameters.length * scale) / 2, offsetY + 120);

    // Road width (PMGSY standard)
    ctx.beginPath();
    ctx.moveTo(offsetX - 20, offsetY + 150);
    ctx.lineTo(offsetX - 20, offsetY + 150 + 3500 * scale);
    ctx.stroke();
    ctx.save();
    ctx.translate(offsetX - 25, offsetY + 150 + (3500 * scale) / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(`3500 mm (PMGSY)`, 0, 0);
    ctx.restore();
  };

  const drawGrid = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 0.5;
    ctx.setLineDash([2, 2]);

    const gridSize = 100 * scale; // 100m grid
    const maxWidth = Math.max(parameters.length * scale, 800);
    const maxHeight = 600;

    for (let x = offsetX; x <= offsetX + maxWidth; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, offsetY);
      ctx.lineTo(x, offsetY + maxHeight);
      ctx.stroke();
    }

    for (let y = offsetY; y <= offsetY + maxHeight; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(offsetX, y);
      ctx.lineTo(offsetX + maxWidth, y);
      ctx.stroke();
    }

    ctx.setLineDash([]);
  };

  const handleParameterChange = (key: keyof RoadParameters, value: number | string) => {
    setParameters(prev => ({ ...prev, [key]: value }));
  };

  const resetParameters = () => {
    setParameters({
      length: 1000,
      interval: 50,
      naturalGroundLevel: 100,
      formationLevel: 98,
      roadWidth: 7000,
      shoulderWidth: 1500,
      scale: 50,
      roadNumber: "R-001"
    });
  };

  const exportDrawing = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const link = document.createElement("a");
    link.download = `road-drawing-${parameters.roadNumber}.png`;
    link.href = canvas.toDataURL();
    link.click();
  };

  const getRoadTypeTitle = () => {
    switch (roadType) {
      case "l-section": return "Road Longitudinal Section";
      case "cross-section": return "Road Cross Section";
      case "plan": return "Road Plan View";
      case "pmgsy": return "PMGSY Road Design";
      default: return "Road Design";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{getRoadTypeTitle()}</h1>
          <p className="text-muted-foreground">
            Generate professional road drawings with customizable parameters
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={resetParameters}>
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
          <Button variant="outline" onClick={exportDrawing}>
            <Download className="w-4 h-4 mr-2" />
            Export Drawing
          </Button>
          <Button>
            <Share2 className="w-4 h-4 mr-2" />
            Share Drawing
          </Button>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="drawing">Drawing Parameters</TabsTrigger>
          <TabsTrigger value="visualization">Drawing View</TabsTrigger>
        </TabsList>

        <TabsContent value="drawing" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Road Dimensions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Road className="w-5 h-5" />
                  <span>Road Dimensions</span>
                </CardTitle>
                <CardDescription>
                  Set the geometric parameters for your road drawing
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="length">Road Length (m)</Label>
                    <Input
                      id="length"
                      type="number"
                      value={parameters.length}
                      onChange={(e) => handleParameterChange("length", Number(e.target.value))}
                      min="100"
                      max="5000"
                      step="50"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="interval">Interval (m)</Label>
                    <Input
                      id="interval"
                      type="number"
                      value={parameters.interval}
                      onChange={(e) => handleParameterChange("interval", Number(e.target.value))}
                      min="10"
                      max="100"
                      step="10"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="roadWidth">Road Width (mm)</Label>
                    <Input
                      id="roadWidth"
                      type="number"
                      value={parameters.roadWidth}
                      onChange={(e) => handleParameterChange("roadWidth", Number(e.target.value))}
                      min="3000"
                      max="12000"
                      step="500"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="shoulderWidth">Shoulder Width (mm)</Label>
                    <Input
                      id="shoulderWidth"
                      type="number"
                      value={parameters.shoulderWidth}
                      onChange={(e) => handleParameterChange("shoulderWidth", Number(e.target.value))}
                      min="500"
                      max="3000"
                      step="100"
                    />
                  </div>
                </div>

                <Separator />

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="naturalGroundLevel">Natural Ground Level (m)</Label>
                    <Input
                      id="naturalGroundLevel"
                      type="number"
                      value={parameters.naturalGroundLevel}
                      onChange={(e) => handleParameterChange("naturalGroundLevel", Number(e.target.value))}
                      min="90"
                      max="110"
                      step="0.5"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="formationLevel">Formation Level (m)</Label>
                    <Input
                      id="formationLevel"
                      type="number"
                      value={parameters.formationLevel}
                      onChange={(e) => handleParameterChange("formationLevel", Number(e.target.value))}
                      min="88"
                      max="108"
                      step="0.5"
                    />
                  </div>
                </div>

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

                <div className="space-y-2">
                  <Label htmlFor="roadNumber">Drawing Number</Label>
                  <Input
                    id="roadNumber"
                    value={parameters.roadNumber}
                    onChange={(e) => handleParameterChange("roadNumber", e.target.value)}
                    placeholder="R-001"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Drawing Options */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Eye className="w-5 h-5" />
                  <span>Drawing Options</span>
                </CardTitle>
                <CardDescription>
                  Customize the appearance of your road drawing
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-4">
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
                      id="showGrid"
                      checked={drawing.showGrid}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showGrid: checked }))}
                    />
                    <Label htmlFor="showGrid">Show Grid</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Switch
                      id="showLevels"
                      checked={drawing.showLevels}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showLevels: checked }))}
                    />
                    <Label htmlFor="showLevels">Show Levels</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Switch
                      id="showCrossSection"
                      checked={drawing.showCrossSection}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showCrossSection: checked }))}
                    />
                    <Label htmlFor="showCrossSection">Show Cross Section</Label>
                  </div>
                </div>

                <Separator />

                <div className="space-y-2">
                  <Label htmlFor="canvasWidth">Canvas Width (px)</Label>
                  <Input
                    id="canvasWidth"
                    type="number"
                    value={drawing.width}
                    onChange={(e) => setDrawing(prev => ({ ...prev, width: Number(e.target.value) }))}
                    min="600"
                    max="1400"
                    step="100"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="canvasHeight">Canvas Height (px)</Label>
                  <Input
                    id="canvasHeight"
                    type="number"
                    value={drawing.height}
                    onChange={(e) => setDrawing(prev => ({ ...prev, height: Number(e.target.value) }))}
                    min="400"
                    max="800"
                    step="50"
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
                <span>Road Drawing</span>
              </CardTitle>
              <CardDescription>
                Real-time 2D representation of your road design
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
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
                <div className="grid grid-cols-4 gap-4 text-sm">
                  <div className="text-center">
                    <div className="font-medium">Scale</div>
                    <div className="text-muted-foreground">1:{parameters.scale}</div>
                  </div>
                  <div className="text-center">
                    <div className="font-medium">Canvas Size</div>
                    <div className="text-muted-foreground">{drawing.width} × {drawing.height} px</div>
                  </div>
                  <div className="text-center">
                    <div className="font-medium">Drawing Number</div>
                    <div className="text-muted-foreground">{parameters.roadNumber}</div>
                  </div>
                  <div className="text-center">
                    <div className="font-medium">Type</div>
                    <div className="text-muted-foreground capitalize">{roadType.replace('-', ' ')}</div>
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
