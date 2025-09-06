import { useState, useRef, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Stairs,
  Download,
  RotateCcw,
  Eye,
  Share2,
  Ruler,
  Layers
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

interface StaircaseParameters {
  totalHeight: number;
  totalWidth: number;
  treadWidth: number;
  riserHeight: number;
  landingWidth: number;
  landingLength: number;
  scale: number;
  staircaseNumber: string;
}

interface StaircaseDrawing {
  width: number;
  height: number;
  scale: number;
  showDimensions: boolean;
  showGrid: boolean;
  showCenterLines: boolean;
  showLanding: boolean;
}

export default function StaircaseDesign() {
  const [searchParams] = useSearchParams();
  const staircaseType = searchParams.get("type") || "straight";
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [parameters, setParameters] = useState<StaircaseParameters>({
    totalHeight: 3000,
    totalWidth: 1200,
    treadWidth: 300,
    riserHeight: 150,
    landingWidth: 1200,
    landingLength: 1200,
    scale: 50,
    staircaseNumber: "S-001"
  });

  const [drawing, setDrawing] = useState<StaircaseDrawing>({
    width: 1000,
    height: 800,
    scale: 50,
    showDimensions: true,
    showGrid: false,
    showCenterLines: true,
    showLanding: true
  });

  const [activeTab, setActiveTab] = useState("drawing");

  // Calculate number of steps
  const numberOfSteps = Math.floor(parameters.totalHeight / parameters.riserHeight);
  const totalRun = numberOfSteps * parameters.treadWidth;

  // Update drawing when parameters change
  useEffect(() => {
    drawStaircase();
  }, [parameters, drawing]);

  const drawStaircase = () => {
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

    if (staircaseType === "straight") {
      drawStraightStaircase(ctx, offsetX, offsetY, scale);
    } else if (staircaseType === "l-shaped") {
      drawLShapedStaircase(ctx, offsetX, offsetY, scale);
    } else if (staircaseType === "u-shaped") {
      drawUShapedStaircase(ctx, offsetX, offsetY, scale);
    } else if (staircaseType === "spiral") {
      drawSpiralStaircase(ctx, offsetX, offsetY, scale);
    }

    // Draw grid if enabled
    if (drawing.showGrid) {
      drawGrid(ctx, offsetX, offsetY, scale);
    }
  };

  const drawStraightStaircase = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    const startX = offsetX;
    const startY = offsetY + 400;
    const stairWidth = parameters.totalWidth * scale;

    // Draw each step
    for (let i = 0; i < numberOfSteps; i++) {
      const stepX = startX + i * parameters.treadWidth * scale;
      const stepY = startY - i * parameters.riserHeight * scale;

      // Draw tread (horizontal part)
      ctx.beginPath();
      ctx.rect(stepX, stepY, parameters.treadWidth * scale, parameters.riserHeight * scale);
      ctx.fill();
      ctx.stroke();

      // Draw riser (vertical part)
      if (i < numberOfSteps - 1) {
        ctx.beginPath();
        ctx.rect(stepX + parameters.treadWidth * scale, stepY, 2, parameters.riserHeight * scale);
        ctx.fill();
        ctx.stroke();
      }
    }

    // Draw landing if enabled
    if (drawing.showLanding) {
      const landingX = startX + totalRun * scale;
      const landingY = startY - parameters.totalHeight * scale;
      
      ctx.fillStyle = "#e5e7eb";
      ctx.beginPath();
      ctx.rect(landingX, landingY, parameters.landingLength * scale, parameters.landingWidth * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw center lines if enabled
    if (drawing.showCenterLines) {
      drawStaircaseCenterLines(ctx, startX, startY, scale);
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawStaircaseDimensions(ctx, startX, startY, scale);
    }
  };

  const drawLShapedStaircase = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    const startX = offsetX;
    const startY = offsetY + 400;
    const stairWidth = parameters.totalWidth * scale;
    const midPoint = Math.floor(numberOfSteps / 2);

    // Draw first half of steps
    for (let i = 0; i < midPoint; i++) {
      const stepX = startX + i * parameters.treadWidth * scale;
      const stepY = startY - i * parameters.riserHeight * scale;

      ctx.beginPath();
      ctx.rect(stepX, stepY, parameters.treadWidth * scale, parameters.riserHeight * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw landing
    if (drawing.showLanding) {
      const landingX = startX + midPoint * parameters.treadWidth * scale;
      const landingY = startY - midPoint * parameters.riserHeight * scale;
      
      ctx.fillStyle = "#e5e7eb";
      ctx.beginPath();
      ctx.rect(landingX, landingY, parameters.landingLength * scale, parameters.landingWidth * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw second half of steps (perpendicular)
    const secondStartX = startX + midPoint * parameters.treadWidth * scale + parameters.landingLength * scale;
    const secondStartY = startY - midPoint * parameters.riserHeight * scale;

    for (let i = midPoint; i < numberOfSteps; i++) {
      const stepX = secondStartX;
      const stepY = secondStartY - (i - midPoint) * parameters.riserHeight * scale;

      ctx.beginPath();
      ctx.rect(stepX, stepY, parameters.treadWidth * scale, parameters.riserHeight * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawLShapedDimensions(ctx, startX, startY, scale, midPoint);
    }
  };

  const drawUShapedStaircase = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    const startX = offsetX;
    const startY = offsetY + 400;
    const stairWidth = parameters.totalWidth * scale;
    const midPoint = Math.floor(numberOfSteps / 2);
    const gapWidth = 600 * scale; // Gap between stair flights

    // Draw left flight
    for (let i = 0; i < midPoint; i++) {
      const stepX = startX;
      const stepY = startY - i * parameters.riserHeight * scale;

      ctx.beginPath();
      ctx.rect(stepX, stepY, parameters.treadWidth * scale, parameters.riserHeight * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw right flight
    for (let i = 0; i < midPoint; i++) {
      const stepX = startX + parameters.treadWidth * scale + gapWidth;
      const stepY = startY - (midPoint - 1 - i) * parameters.riserHeight * scale;

      ctx.beginPath();
      ctx.rect(stepX, stepY, parameters.treadWidth * scale, parameters.riserHeight * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw landing
    if (drawing.showLanding) {
      const landingX = startX;
      const landingY = startY - midPoint * parameters.riserHeight * scale;
      
      ctx.fillStyle = "#e5e7eb";
      ctx.beginPath();
      ctx.rect(landingX, landingY, parameters.treadWidth * scale + gapWidth, parameters.landingWidth * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawUShapedDimensions(ctx, startX, startY, scale, midPoint, gapWidth);
    }
  };

  const drawSpiralStaircase = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    const centerX = offsetX + 400;
    const centerY = offsetY + 400;
    const radius = 200 * scale;
    const stepAngle = (2 * Math.PI) / numberOfSteps;

    // Draw spiral steps
    for (let i = 0; i < numberOfSteps; i++) {
      const angle1 = i * stepAngle;
      const angle2 = (i + 1) * stepAngle;
      const r1 = radius + (i * 20 * scale);
      const r2 = radius + ((i + 1) * 20 * scale);

      ctx.beginPath();
      ctx.moveTo(centerX + r1 * Math.cos(angle1), centerY + r1 * Math.sin(angle1));
      ctx.lineTo(centerX + r2 * Math.cos(angle1), centerY + r2 * Math.sin(angle1));
      ctx.lineTo(centerX + r2 * Math.cos(angle2), centerY + r2 * Math.sin(angle2));
      ctx.lineTo(centerX + r1 * Math.cos(angle2), centerY + r1 * Math.sin(angle2));
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }

    // Draw center column
    ctx.fillStyle = "#374151";
    ctx.beginPath();
    ctx.arc(centerX, centerY, 30 * scale, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawSpiralDimensions(ctx, centerX, centerY, scale);
    }
  };

  const drawStaircaseCenterLines = (ctx: CanvasRenderingContext2D, startX: number, startY: number, scale: number) => {
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 1;
    ctx.setLineDash([10, 5]);

    // Vertical center line
    const centerX = startX + (parameters.totalWidth * scale) / 2;
    ctx.beginPath();
    ctx.moveTo(centerX, startY - parameters.totalHeight * scale - 50);
    ctx.lineTo(centerX, startY + 50);
    ctx.stroke();

    // Horizontal center line
    const centerY = startY - (parameters.totalHeight * scale) / 2;
    ctx.beginPath();
    ctx.moveTo(startX - 50, centerY);
    ctx.lineTo(startX + totalRun * scale + 50, centerY);
    ctx.stroke();

    ctx.setLineDash([]);
  };

  const drawStaircaseDimensions = (ctx: CanvasRenderingContext2D, startX: number, startY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Total height
    ctx.beginPath();
    ctx.moveTo(startX - 30, startY);
    ctx.lineTo(startX - 30, startY - parameters.totalHeight * scale);
    ctx.stroke();
    ctx.save();
    ctx.translate(startX - 35, startY - (parameters.totalHeight * scale) / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(`${parameters.totalHeight} mm`, 0, 0);
    ctx.restore();

    // Total width
    ctx.beginPath();
    ctx.moveTo(startX, startY + 30);
    ctx.lineTo(startX + parameters.totalWidth * scale, startY + 30);
    ctx.stroke();
    ctx.fillText(`${parameters.totalWidth} mm`, startX + (parameters.totalWidth * scale) / 2, startY + 45);

    // Step dimensions
    ctx.fillText(`Tread: ${parameters.treadWidth} mm`, startX + 100, startY + 60);
    ctx.fillText(`Riser: ${parameters.riserHeight} mm`, startX + 100, startY + 75);
    ctx.fillText(`Steps: ${numberOfSteps}`, startX + 100, startY + 90);
  };

  const drawLShapedDimensions = (ctx: CanvasRenderingContext2D, startX: number, startY: number, scale: number, midPoint: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Total Height: ${parameters.totalHeight} mm`, startX + 200, startY + 60);
    ctx.fillText(`Steps: ${numberOfSteps}`, startX + 200, startY + 75);
    ctx.fillText(`Type: L-Shaped`, startX + 200, startY + 90);
  };

  const drawUShapedDimensions = (ctx: CanvasRenderingContext2D, startX: number, startY: number, scale: number, midPoint: number, gapWidth: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Total Height: ${parameters.totalHeight} mm`, startX + 300, startY + 60);
    ctx.fillText(`Steps: ${numberOfSteps}`, startX + 300, startY + 75);
    ctx.fillText(`Type: U-Shaped`, startX + 300, startY + 90);
  };

  const drawSpiralDimensions = (ctx: CanvasRenderingContext2D, centerX: number, centerY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Total Height: ${parameters.totalHeight} mm`, centerX, centerY + 300);
    ctx.fillText(`Steps: ${numberOfSteps}`, centerX, centerY + 315);
    ctx.fillText(`Type: Spiral`, centerX, centerY + 330);
  };

  const drawGrid = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 0.5;
    ctx.setLineDash([2, 2]);

    const gridSize = 100 * scale; // 100mm grid
    const maxWidth = Math.max(totalRun * scale, 800);
    const maxHeight = 800;

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

  const handleParameterChange = (key: keyof StaircaseParameters, value: number | string) => {
    setParameters(prev => ({ ...prev, [key]: value }));
  };

  const resetParameters = () => {
    setParameters({
      totalHeight: 3000,
      totalWidth: 1200,
      treadWidth: 300,
      riserHeight: 150,
      landingWidth: 1200,
      landingLength: 1200,
      scale: 50,
      staircaseNumber: "S-001"
    });
  };

  const exportDrawing = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const link = document.createElement("a");
    link.download = `staircase-drawing-${parameters.staircaseNumber}.png`;
    link.href = canvas.toDataURL();
    link.click();
  };

  const getStaircaseTypeTitle = () => {
    switch (staircaseType) {
      case "straight": return "Straight Staircase";
      case "l-shaped": return "L-Shaped Staircase";
      case "u-shaped": return "U-Shaped Staircase";
      case "spiral": return "Spiral Staircase";
      default: return "Staircase Design";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{getStaircaseTypeTitle()}</h1>
          <p className="text-muted-foreground">
            Generate professional staircase drawings with customizable parameters
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
            {/* Staircase Dimensions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Stairs className="w-5 h-5" />
                  <span>Staircase Dimensions</span>
                </CardTitle>
                <CardDescription>
                  Set the geometric parameters for your staircase drawing
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="totalHeight">Total Height (mm)</Label>
                    <Input
                      id="totalHeight"
                      type="number"
                      value={parameters.totalHeight}
                      onChange={(e) => handleParameterChange("totalHeight", Number(e.target.value))}
                      min="2000"
                      max="5000"
                      step="100"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="totalWidth">Total Width (mm)</Label>
                    <Input
                      id="totalWidth"
                      type="number"
                      value={parameters.totalWidth}
                      onChange={(e) => handleParameterChange("totalWidth", Number(e.target.value))}
                      min="800"
                      max="2000"
                      step="100"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="treadWidth">Tread Width (mm)</Label>
                    <Input
                      id="treadWidth"
                      type="number"
                      value={parameters.treadWidth}
                      onChange={(e) => handleParameterChange("treadWidth", Number(e.target.value))}
                      min="200"
                      max="400"
                      step="25"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="riserHeight">Riser Height (mm)</Label>
                    <Input
                      id="riserHeight"
                      type="number"
                      value={parameters.riserHeight}
                      onChange={(e) => handleParameterChange("riserHeight", Number(e.target.value))}
                      min="100"
                      max="200"
                      step="25"
                    />
                  </div>
                </div>

                <Separator />

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="landingWidth">Landing Width (mm)</Label>
                    <Input
                      id="landingWidth"
                      type="number"
                      value={parameters.landingWidth}
                      onChange={(e) => handleParameterChange("landingWidth", Number(e.target.value))}
                      min="800"
                      max="2000"
                      step="100"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="landingLength">Landing Length (mm)</Label>
                    <Input
                      id="landingLength"
                      type="number"
                      value={parameters.landingLength}
                      onChange={(e) => handleParameterChange("landingLength", Number(e.target.value))}
                      min="800"
                      max="2000"
                      step="100"
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
                  <Label htmlFor="staircaseNumber">Drawing Number</Label>
                  <Input
                    id="staircaseNumber"
                    value={parameters.staircaseNumber}
                    onChange={(e) => handleParameterChange("staircaseNumber", e.target.value)}
                    placeholder="S-001"
                  />
                </div>

                {/* Calculated Values */}
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">Calculated Values</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm text-blue-800">
                    <div>
                      <span className="font-medium">Number of Steps:</span> {numberOfSteps}
                    </div>
                    <div>
                      <span className="font-medium">Total Run:</span> {totalRun} mm
                    </div>
                    <div>
                      <span className="font-medium">Step Ratio:</span> {(parameters.treadWidth + parameters.riserHeight * 2).toFixed(0)} mm
                    </div>
                    <div>
                      <span className="font-medium">Type:</span> {getStaircaseTypeTitle()}
                    </div>
                  </div>
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
                  Customize the appearance of your staircase drawing
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
                      id="showCenterLines"
                      checked={drawing.showCenterLines}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showCenterLines: checked }))}
                    />
                    <Label htmlFor="showCenterLines">Show Center Lines</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Switch
                      id="showLanding"
                      checked={drawing.showLanding}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showLanding: checked }))}
                    />
                    <Label htmlFor="showLanding">Show Landing</Label>
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
                    min="800"
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
                    min="600"
                    max="1000"
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
                <span>Staircase Drawing</span>
              </CardTitle>
              <CardDescription>
                Real-time 2D representation of your staircase design
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
                    <div className="text-muted-foreground">{parameters.staircaseNumber}</div>
                  </div>
                  <div className="text-center">
                    <div className="font-medium">Type</div>
                    <div className="text-muted-foreground capitalize">{staircaseType.replace('-', ' ')}</div>
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
