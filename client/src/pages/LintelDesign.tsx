import { useState, useRef, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Ruler,
  RotateCcw,
  Eye,
  Share2,
  Building2,
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
import ExportDropdown from "@/components/ExportDropdown";

interface LintelParameters {
  width: number;
  height: number;
  thickness: number;
  openingWidth: number;
  openingHeight: number;
  wallThickness: number;
  scale: number;
  lintelNumber: string;
}

interface LintelDrawing {
  width: number;
  height: number;
  scale: number;
  showDimensions: boolean;
  showGrid: boolean;
  showReinforcement: boolean;
  showCenterLines: boolean;
}

export default function LintelDesign() {
  const [searchParams] = useSearchParams();
  const lintelType = searchParams.get("type") || "concrete";
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [parameters, setParameters] = useState<LintelParameters>({
    width: 3000,
    height: 300,
    thickness: 200,
    openingWidth: 1200,
    openingHeight: 2100,
    wallThickness: 230,
    scale: 50,
    lintelNumber: "L-001"
  });

  const [drawing, setDrawing] = useState<LintelDrawing>({
    width: 1000,
    height: 800,
    scale: 50,
    showDimensions: true,
    showGrid: false,
    showReinforcement: false,
    showCenterLines: true
  });

  const [activeTab, setActiveTab] = useState("drawing");

  // Update drawing when parameters change
  useEffect(() => {
    drawLintel();
  }, [parameters, drawing]);

  const drawLintel = () => {
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

    if (lintelType === "concrete") {
      drawConcreteLintel(ctx, offsetX, offsetY, scale);
    } else if (lintelType === "steel") {
      drawSteelLintel(ctx, offsetX, offsetY, scale);
    } else if (lintelType === "precast") {
      drawPrecastLintel(ctx, offsetX, offsetY, scale);
    } else if (lintelType === "arch") {
      drawArchLintel(ctx, offsetX, offsetY, scale);
    }

    // Draw grid if enabled
    if (drawing.showGrid) {
      drawGrid(ctx, offsetX, offsetY, scale);
    }
  };

  const drawConcreteLintel = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw wall
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, parameters.width * scale, parameters.wallThickness * scale);
    ctx.fill();
    ctx.stroke();

    // Draw lintel beam
    ctx.fillStyle = "#e5e7eb";
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, parameters.width * scale, parameters.height * scale);
    ctx.fill();
    ctx.stroke();

    // Draw opening
    const openingX = offsetX + (parameters.width - parameters.openingWidth) * scale / 2;
    const openingY = offsetY + 200 + parameters.height * scale;
    ctx.fillStyle = "#ffffff";
    ctx.beginPath();
    ctx.rect(openingX, openingY, parameters.openingWidth * scale, parameters.openingHeight * scale);
    ctx.fill();
    ctx.stroke();

    // Draw reinforcement if enabled
    if (drawing.showReinforcement) {
      drawLintelReinforcement(ctx, offsetX, offsetY, scale);
    }

    // Draw center lines if enabled
    if (drawing.showCenterLines) {
      drawLintelCenterLines(ctx, offsetX, offsetY, scale);
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawConcreteLintelDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawSteelLintel = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw wall
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, parameters.width * scale, parameters.wallThickness * scale);
    ctx.fill();
    ctx.stroke();

    // Draw steel lintel (I-beam shape)
    ctx.fillStyle = "#6b7280";
    const beamX = offsetX;
    const beamY = offsetY + 200;
    
    // Draw I-beam
    ctx.beginPath();
    ctx.rect(beamX, beamY, parameters.width * scale, parameters.height * scale);
    ctx.fill();
    ctx.stroke();

    // Draw I-beam flanges
    ctx.fillStyle = "#374151";
    const flangeHeight = parameters.height * scale * 0.2;
    ctx.beginPath();
    ctx.rect(beamX, beamY, parameters.width * scale, flangeHeight);
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.rect(beamX, beamY + parameters.height * scale - flangeHeight, parameters.width * scale, flangeHeight);
    ctx.fill();
    ctx.stroke();

    // Draw opening
    const openingX = offsetX + (parameters.width - parameters.openingWidth) * scale / 2;
    const openingY = offsetY + 200 + parameters.height * scale;
    ctx.fillStyle = "#ffffff";
    ctx.beginPath();
    ctx.rect(openingX, openingY, parameters.openingWidth * scale, parameters.openingHeight * scale);
    ctx.fill();
    ctx.stroke();

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawSteelLintelDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawPrecastLintel = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw wall
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, parameters.width * scale, parameters.wallThickness * scale);
    ctx.fill();
    ctx.stroke();

    // Draw precast lintel blocks
    const blockWidth = 600 * scale;
    const blockCount = Math.ceil(parameters.width / 600);
    
    for (let i = 0; i < blockCount; i++) {
      const blockX = offsetX + i * blockWidth;
      const blockY = offsetY + 200;
      
      ctx.fillStyle = "#e5e7eb";
      ctx.beginPath();
      ctx.rect(blockX, blockY, Math.min(blockWidth, (parameters.width - i * 600) * scale), parameters.height * scale);
      ctx.fill();
      ctx.stroke();

      // Draw block separators
      if (i < blockCount - 1) {
        ctx.strokeStyle = "#6b7280";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(blockX + blockWidth, blockY);
        ctx.lineTo(blockX + blockWidth, blockY + parameters.height * scale);
        ctx.stroke();
      }
    }

    // Draw opening
    const openingX = offsetX + (parameters.width - parameters.openingWidth) * scale / 2;
    const openingY = offsetY + 200 + parameters.height * scale;
    ctx.fillStyle = "#ffffff";
    ctx.beginPath();
    ctx.rect(openingX, openingY, parameters.openingWidth * scale, parameters.openingHeight * scale);
    ctx.fill();
    ctx.stroke();

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawPrecastLintelDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawArchLintel = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw wall
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, parameters.width * scale, parameters.wallThickness * scale);
    ctx.fill();
    ctx.stroke();

    // Draw arch lintel
    ctx.fillStyle = "#e5e7eb";
    const archCenterX = offsetX + parameters.width * scale / 2;
    const archCenterY = offsetY + 200 + parameters.height * scale;
    const archRadius = parameters.openingWidth * scale / 2;
    
    ctx.beginPath();
    ctx.arc(archCenterX, archCenterY, archRadius, 0, Math.PI, true);
    ctx.lineTo(archCenterX - archRadius, archCenterY);
    ctx.lineTo(archCenterX - archRadius, archCenterY - parameters.height * scale);
    ctx.lineTo(archCenterX + archRadius, archCenterY - parameters.height * scale);
    ctx.lineTo(archCenterX + archRadius, archCenterY);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Draw opening
    const openingX = offsetX + (parameters.width - parameters.openingWidth) * scale / 2;
    const openingY = offsetY + 200 + parameters.height * scale;
    ctx.fillStyle = "#ffffff";
    ctx.beginPath();
    ctx.rect(openingX, openingY, parameters.openingWidth * scale, parameters.openingHeight * scale);
    ctx.fill();
    ctx.stroke();

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawArchLintelDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawLintelReinforcement = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);

    // Draw main reinforcement bars
    const barSpacing = 200 * scale;
    for (let x = offsetX; x <= offsetX + parameters.width * scale; x += barSpacing) {
      ctx.beginPath();
      ctx.moveTo(x, offsetY + 200);
      ctx.lineTo(x, offsetY + 200 + parameters.height * scale);
      ctx.stroke();
    }

    // Draw distribution bars
    for (let y = offsetY + 200; y <= offsetY + 200 + parameters.height * scale; y += barSpacing) {
      ctx.beginPath();
      ctx.moveTo(offsetX, y);
      ctx.lineTo(offsetX + parameters.width * scale, y);
      ctx.stroke();
    }

    ctx.setLineDash([]);
  };

  const drawLintelCenterLines = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 1;
    ctx.setLineDash([10, 5]);

    // Vertical center line
    const centerX = offsetX + (parameters.width * scale) / 2;
    ctx.beginPath();
    ctx.moveTo(centerX, offsetY + 200 - 50);
    ctx.lineTo(centerX, offsetY + 200 + parameters.wallThickness * scale + 50);
    ctx.stroke();

    // Horizontal center line
    const centerY = offsetY + 200 + (parameters.wallThickness * scale) / 2;
    ctx.beginPath();
    ctx.moveTo(offsetX - 50, centerY);
    ctx.lineTo(offsetX + parameters.width * scale + 50, centerY);
    ctx.stroke();

    ctx.setLineDash([]);
  };

  const drawConcreteLintelDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Lintel width
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY + 150);
    ctx.lineTo(offsetX + parameters.width * scale, offsetY + 150);
    ctx.stroke();
    ctx.fillText(`${parameters.width} mm`, offsetX + (parameters.width * scale) / 2, offsetY + 140);

    // Lintel height
    ctx.beginPath();
    ctx.moveTo(offsetX - 30, offsetY + 200);
    ctx.lineTo(offsetX - 30, offsetY + 200 + parameters.height * scale);
    ctx.stroke();
    ctx.save();
    ctx.translate(offsetX - 35, offsetY + 200 + (parameters.height * scale) / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(`${parameters.height} mm`, 0, 0);
    ctx.restore();

    // Opening dimensions
    const openingX = offsetX + (parameters.width - parameters.openingWidth) * scale / 2;
    const openingY = offsetY + 200 + parameters.height * scale;
    
    ctx.beginPath();
    ctx.moveTo(openingX, openingY + parameters.openingHeight * scale + 20);
    ctx.lineTo(openingX + parameters.openingWidth * scale, openingY + parameters.openingHeight * scale + 20);
    ctx.stroke();
    ctx.fillText(`${parameters.openingWidth} mm`, openingX + (parameters.openingWidth * scale) / 2, openingY + parameters.openingHeight * scale + 35);

    ctx.beginPath();
    ctx.moveTo(openingX - 20, openingY);
    ctx.lineTo(openingX - 20, openingY + parameters.openingHeight * scale);
    ctx.stroke();
    ctx.save();
    ctx.translate(openingX - 25, openingY + (parameters.openingHeight * scale) / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(`${parameters.openingHeight} mm`, 0, 0);
    ctx.restore();
  };

  const drawSteelLintelDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Width: ${parameters.width} mm`, offsetX + 300, offsetY + 150);
    ctx.fillText(`Height: ${parameters.height} mm`, offsetX + 300, offsetY + 165);
    ctx.fillText(`Type: Steel I-Beam`, offsetX + 300, offsetY + 180);
  };

  const drawPrecastLintelDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Width: ${parameters.width} mm`, offsetX + 300, offsetY + 150);
    ctx.fillText(`Height: ${parameters.height} mm`, offsetX + 300, offsetY + 165);
    ctx.fillText(`Type: Precast Blocks`, offsetX + 300, offsetY + 180);
  };

  const drawArchLintelDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Width: ${parameters.width} mm`, offsetX + 300, offsetY + 150);
    ctx.fillText(`Height: ${parameters.height} mm`, offsetX + 300, offsetY + 165);
    ctx.fillText(`Type: Arch Lintel`, offsetX + 300, offsetY + 180);
  };

  const drawGrid = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 0.5;
    ctx.setLineDash([2, 2]);

    const gridSize = 100 * scale; // 100mm grid
    const maxWidth = Math.max(parameters.width * scale, 800);
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

  const handleParameterChange = (key: keyof LintelParameters, value: number | string) => {
    setParameters(prev => ({ ...prev, [key]: value }));
  };

  const resetParameters = () => {
    setParameters({
      width: 3000,
      height: 300,
      thickness: 200,
      openingWidth: 1200,
      openingHeight: 2100,
      wallThickness: 230,
      scale: 50,
      lintelNumber: "L-001"
    });
  };

  const getExportOptions = () => ({
    filename: `lintel-drawing-${parameters.lintelNumber}`,
    title: `${getLintelTypeTitle()} - ${parameters.lintelNumber}`,
    author: "LISP Canvas",
    subject: "Lintel Design Drawing",
    keywords: ["lintel", "design", "drawing", "construction", "architecture"]
  });

  const getLintelTypeTitle = () => {
    switch (lintelType) {
      case "concrete": return "Concrete Lintel";
      case "steel": return "Steel Lintel";
      case "precast": return "Precast Lintel";
      case "arch": return "Arch Lintel";
      default: return "Lintel Design";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{getLintelTypeTitle()}</h1>
          <p className="text-muted-foreground">
            Generate professional lintel drawings with customizable parameters
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={resetParameters}>
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
          <ExportDropdown
            canvas={canvasRef.current}
            filename={`lintel-drawing-${parameters.lintelNumber}`}
            title={`${getLintelTypeTitle()} - ${parameters.lintelNumber}`}
            author="LISP Canvas"
            subject="Lintel Design Drawing"
            keywords={["lintel", "design", "drawing", "construction", "architecture"]}
          />
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
            {/* Lintel Dimensions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Ruler className="w-5 h-5" />
                  <span>Lintel Dimensions</span>
                </CardTitle>
                <CardDescription>
                  Set the geometric parameters for your lintel drawing
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="width">Lintel Width (mm)</Label>
                    <Input
                      id="width"
                      type="number"
                      value={parameters.width}
                      onChange={(e) => handleParameterChange("width", Number(e.target.value))}
                      min="1500"
                      max="6000"
                      step="100"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="height">Lintel Height (mm)</Label>
                    <Input
                      id="height"
                      type="number"
                      value={parameters.height}
                      onChange={(e) => handleParameterChange("height", Number(e.target.value))}
                      min="200"
                      max="500"
                      step="25"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="thickness">Lintel Thickness (mm)</Label>
                    <Input
                      id="thickness"
                      type="number"
                      value={parameters.thickness}
                      onChange={(e) => handleParameterChange("thickness", Number(e.target.value))}
                      min="150"
                      max="400"
                      step="25"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="wallThickness">Wall Thickness (mm)</Label>
                    <Input
                      id="wallThickness"
                      type="number"
                      value={parameters.wallThickness}
                      onChange={(e) => handleParameterChange("wallThickness", Number(e.target.value))}
                      min="200"
                      max="400"
                      step="25"
                    />
                  </div>
                </div>

                <Separator />

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="openingWidth">Opening Width (mm)</Label>
                    <Input
                      id="openingWidth"
                      type="number"
                      value={parameters.openingWidth}
                      onChange={(e) => handleParameterChange("openingWidth", Number(e.target.value))}
                      min="600"
                      max="3000"
                      step="100"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="openingHeight">Opening Height (mm)</Label>
                    <Input
                      id="openingHeight"
                      type="number"
                      value={parameters.openingHeight}
                      onChange={(e) => handleParameterChange("openingHeight", Number(e.target.value))}
                      min="1500"
                      max="3000"
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
                  <Label htmlFor="lintelNumber">Drawing Number</Label>
                  <Input
                    id="lintelNumber"
                    value={parameters.lintelNumber}
                    onChange={(e) => handleParameterChange("lintelNumber", e.target.value)}
                    placeholder="L-001"
                  />
                </div>

                {/* Calculated Values */}
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">Calculated Values</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm text-blue-800">
                    <div>
                      <span className="font-medium">Type:</span> {getLintelTypeTitle()}
                    </div>
                    <div>
                      <span className="font-medium">Area:</span> {((parameters.width * parameters.height) / 1000000).toFixed(3)} m²
                    </div>
                    <div>
                      <span className="font-medium">Volume:</span> {((parameters.width * parameters.height * parameters.thickness) / 1000000000).toFixed(4)} m³
                    </div>
                    <div>
                      <span className="font-medium">Opening Area:</span> {((parameters.openingWidth * parameters.openingHeight) / 1000000).toFixed(2)} m²
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
                  Customize the appearance of your lintel drawing
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
                      id="showReinforcement"
                      checked={drawing.showReinforcement}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showReinforcement: checked }))}
                    />
                    <Label htmlFor="showReinforcement">Show Reinforcement</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Switch
                      id="showCenterLines"
                      checked={drawing.showCenterLines}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showCenterLines: checked }))}
                    />
                    <Label htmlFor="showCenterLines">Show Center Lines</Label>
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
                <span>Lintel Drawing</span>
              </CardTitle>
              <CardDescription>
                Real-time 2D representation of your lintel design
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
                    <div className="text-muted-foreground">{parameters.lintelNumber}</div>
                  </div>
                  <div className="text-center">
                    <div className="font-medium">Type</div>
                    <div className="text-muted-foreground capitalize">{lintelType.replace('-', ' ')}</div>
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
