import { useState, useRef, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Sun,
  RotateCcw,
  Eye,
  Share2,
  Ruler,
  Building2
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

interface SunshadeParameters {
  width: number;
  projection: number;
  thickness: number;
  beamWidth: number;
  beamDepth: number;
  beamSpacing: number;
  scale: number;
  sunshadeNumber: string;
}

interface SunshadeDrawing {
  width: number;
  height: number;
  scale: number;
  showDimensions: boolean;
  showGrid: boolean;
  showBeams: boolean;
  showReinforcement: boolean;
}

export default function SunshadeDesign() {
  const [searchParams] = useSearchParams();
  const sunshadeType = searchParams.get("type") || "cantilever";
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [parameters, setParameters] = useState<SunshadeParameters>({
    width: 3000,
    projection: 1200,
    thickness: 150,
    beamWidth: 300,
    beamDepth: 300,
    beamSpacing: 600,
    scale: 50,
    sunshadeNumber: "SS-001"
  });

  const [drawing, setDrawing] = useState<SunshadeDrawing>({
    width: 1000,
    height: 800,
    scale: 50,
    showDimensions: true,
    showGrid: false,
    showBeams: true,
    showReinforcement: false
  });

  const [activeTab, setActiveTab] = useState("drawing");

  // Calculate number of beams
  const numberOfBeams = Math.floor(parameters.width / parameters.beamSpacing) + 1;

  // Update drawing when parameters change
  useEffect(() => {
    drawSunshade();
  }, [parameters, drawing]);

  const drawSunshade = () => {
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

    if (sunshadeType === "cantilever") {
      drawCantileverSunshade(ctx, offsetX, offsetY, scale);
    } else if (sunshadeType === "supported") {
      drawSupportedSunshade(ctx, offsetX, offsetY, scale);
    } else if (sunshadeType === "folding") {
      drawFoldingSunshade(ctx, offsetX, offsetY, scale);
    } else if (sunshadeType === "retractable") {
      drawRetractableSunshade(ctx, offsetX, offsetY, scale);
    }

    // Draw grid if enabled
    if (drawing.showGrid) {
      drawGrid(ctx, offsetX, offsetY, scale);
    }
  };

  const drawCantileverSunshade = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw wall
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, 100 * scale, 400 * scale);
    ctx.fill();
    ctx.stroke();

    // Draw sunshade slab
    ctx.beginPath();
    ctx.rect(offsetX + 100 * scale, offsetY + 200, parameters.projection * scale, parameters.thickness * scale);
    ctx.fill();
    ctx.stroke();

    // Draw beams if enabled
    if (drawing.showBeams) {
      drawSunshadeBeams(ctx, offsetX, offsetY, scale);
    }

    // Draw reinforcement if enabled
    if (drawing.showReinforcement) {
      drawSunshadeReinforcement(ctx, offsetX, offsetY, scale);
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawCantileverDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawSupportedSunshade = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw wall
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, 100 * scale, 400 * scale);
    ctx.fill();
    ctx.stroke();

    // Draw sunshade slab
    ctx.beginPath();
    ctx.rect(offsetX + 100 * scale, offsetY + 200, parameters.projection * scale, parameters.thickness * scale);
    ctx.fill();
    ctx.stroke();

    // Draw support columns
    const columnSpacing = parameters.width / (numberOfBeams + 1);
    for (let i = 0; i < numberOfBeams; i++) {
      const columnX = offsetX + 100 * scale + (i + 1) * columnSpacing * scale;
      ctx.beginPath();
      ctx.rect(columnX - 75 * scale, offsetY + 200 + parameters.thickness * scale, 150 * scale, 200 * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw beams if enabled
    if (drawing.showBeams) {
      drawSunshadeBeams(ctx, offsetX, offsetY, scale);
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawSupportedDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawFoldingSunshade = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw wall
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, 100 * scale, 400 * scale);
    ctx.fill();
    ctx.stroke();

    // Draw multiple folding panels
    const panelWidth = parameters.projection / 3;
    for (let i = 0; i < 3; i++) {
      const panelX = offsetX + 100 * scale + i * panelWidth * scale;
      ctx.beginPath();
      ctx.rect(panelX, offsetY + 200, panelWidth * scale, parameters.thickness * scale);
      ctx.fill();
      ctx.stroke();

      // Draw hinge lines
      if (i < 2) {
        ctx.strokeStyle = "#dc2626";
        ctx.lineWidth = 1;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(panelX + panelWidth * scale, offsetY + 200);
        ctx.lineTo(panelX + panelWidth * scale, offsetY + 200 + parameters.thickness * scale);
        ctx.stroke();
        ctx.setLineDash([]);
      }
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawFoldingDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawRetractableSunshade = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw wall
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, 100 * scale, 400 * scale);
    ctx.fill();
    ctx.stroke();

    // Draw retractable mechanism
    ctx.beginPath();
    ctx.rect(offsetX + 100 * scale, offsetY + 200, 200 * scale, 50 * scale);
    ctx.fill();
    ctx.stroke();

    // Draw retractable panels
    const panelCount = 4;
    const panelWidth = (parameters.projection - 200) / panelCount;
    for (let i = 0; i < panelCount; i++) {
      const panelX = offsetX + 300 * scale + i * panelWidth * scale;
      ctx.beginPath();
      ctx.rect(panelX, offsetY + 200, panelWidth * scale, parameters.thickness * scale);
      ctx.fill();
      ctx.stroke();

      // Draw panel separators
      if (i < panelCount - 1) {
        ctx.strokeStyle = "#6b7280";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(panelX + panelWidth * scale, offsetY + 200);
        ctx.lineTo(panelX + panelWidth * scale, offsetY + 200 + parameters.thickness * scale);
        ctx.stroke();
      }
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawRetractableDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawSunshadeBeams = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#374151";
    ctx.lineWidth = 1;
    ctx.fillStyle = "#e5e7eb";

    // Draw support beams
    for (let i = 0; i < numberOfBeams; i++) {
      const beamX = offsetX + 100 * scale + i * parameters.beamSpacing * scale;
      ctx.beginPath();
      ctx.rect(beamX, offsetY + 200 + parameters.thickness * scale, parameters.beamWidth * scale, parameters.beamDepth * scale);
      ctx.fill();
      ctx.stroke();
    }
  };

  const drawSunshadeReinforcement = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);

    // Draw main reinforcement bars
    const barSpacing = 200 * scale;
    for (let x = offsetX + 100 * scale; x <= offsetX + 100 * scale + parameters.projection * scale; x += barSpacing) {
      ctx.beginPath();
      ctx.moveTo(x, offsetY + 200);
      ctx.lineTo(x, offsetY + 200 + parameters.thickness * scale);
      ctx.stroke();
    }

    // Draw distribution bars
    for (let y = offsetY + 200; y <= offsetY + 200 + parameters.thickness * scale; y += barSpacing) {
      ctx.beginPath();
      ctx.moveTo(offsetX + 100 * scale, y);
      ctx.lineTo(offsetX + 100 * scale + parameters.projection * scale, y);
      ctx.stroke();
    }

    ctx.setLineDash([]);
  };

  const drawCantileverDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Width dimension
    ctx.beginPath();
    ctx.moveTo(offsetX + 100 * scale, offsetY + 150);
    ctx.lineTo(offsetX + 100 * scale + parameters.width * scale, offsetY + 150);
    ctx.stroke();
    ctx.fillText(`${parameters.width} mm`, offsetX + 100 * scale + (parameters.width * scale) / 2, offsetY + 140);

    // Projection dimension
    ctx.beginPath();
    ctx.moveTo(offsetX + 100 * scale + parameters.projection * scale, offsetY + 200);
    ctx.lineTo(offsetX + 100 * scale + parameters.projection * scale, offsetY + 180);
    ctx.lineTo(offsetX + 100 * scale, offsetY + 180);
    ctx.lineTo(offsetX + 100 * scale, offsetY + 200);
    ctx.stroke();
    ctx.fillText(`${parameters.projection} mm`, offsetX + 100 * scale + (parameters.projection * scale) / 2, offsetY + 170);

    // Thickness dimension
    ctx.beginPath();
    ctx.moveTo(offsetX + 80, offsetY + 200);
    ctx.lineTo(offsetX + 80, offsetY + 200 + parameters.thickness * scale);
    ctx.stroke();
    ctx.save();
    ctx.translate(offsetX + 75, offsetY + 200 + (parameters.thickness * scale) / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(`${parameters.thickness} mm`, 0, 0);
    ctx.restore();
  };

  const drawSupportedDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Width: ${parameters.width} mm`, offsetX + 300, offsetY + 150);
    ctx.fillText(`Projection: ${parameters.projection} mm`, offsetX + 300, offsetY + 165);
    ctx.fillText(`Type: Supported`, offsetX + 300, offsetY + 180);
  };

  const drawFoldingDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Width: ${parameters.width} mm`, offsetX + 300, offsetY + 150);
    ctx.fillText(`Projection: ${parameters.projection} mm`, offsetX + 300, offsetY + 165);
    ctx.fillText(`Type: Folding`, offsetX + 300, offsetY + 180);
  };

  const drawRetractableDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Width: ${parameters.width} mm`, offsetX + 300, offsetY + 150);
    ctx.fillText(`Projection: ${parameters.projection} mm`, offsetX + 300, offsetY + 165);
    ctx.fillText(`Type: Retractable`, offsetX + 300, offsetY + 180);
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

  const handleParameterChange = (key: keyof SunshadeParameters, value: number | string) => {
    setParameters(prev => ({ ...prev, [key]: value }));
  };

  const resetParameters = () => {
    setParameters({
      width: 3000,
      projection: 1200,
      thickness: 150,
      beamWidth: 300,
      beamDepth: 300,
      beamSpacing: 600,
      scale: 50,
      sunshadeNumber: "SS-001"
    });
  };

  const getExportOptions = () => ({
    filename: `sunshade-drawing-${parameters.sunshadeNumber}`,
    title: `${getSunshadeTypeTitle()} - ${parameters.sunshadeNumber}`,
    author: "LISP Canvas",
    subject: "Sunshade Design Drawing",
    keywords: ["sunshade", "design", "drawing", "construction", "architecture"]
  });

  const getSunshadeTypeTitle = () => {
    switch (sunshadeType) {
      case "cantilever": return "Cantilever Sunshade";
      case "supported": return "Supported Sunshade";
      case "folding": return "Folding Sunshade";
      case "retractable": return "Retractable Sunshade";
      default: return "Sunshade Design";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{getSunshadeTypeTitle()}</h1>
          <p className="text-muted-foreground">
            Generate professional sunshade drawings with customizable parameters
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={resetParameters}>
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
          <ExportDropdown
            canvas={canvasRef.current}
            filename={`sunshade-drawing-${parameters.sunshadeNumber}`}
            title={`${getSunshadeTypeTitle()} - ${parameters.sunshadeNumber}`}
            author="LISP Canvas"
            subject="Sunshade Design Drawing"
            keywords={["sunshade", "design", "drawing", "construction", "architecture"]}
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
            {/* Sunshade Dimensions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Sun className="w-5 h-5" />
                  <span>Sunshade Dimensions</span>
                </CardTitle>
                <CardDescription>
                  Set the geometric parameters for your sunshade drawing
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="width">Width (mm)</Label>
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
                    <Label htmlFor="projection">Projection (mm)</Label>
                    <Input
                      id="projection"
                      type="number"
                      value={parameters.projection}
                      onChange={(e) => handleParameterChange("projection", Number(e.target.value))}
                      min="600"
                      max="2000"
                      step="100"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="thickness">Slab Thickness (mm)</Label>
                    <Input
                      id="thickness"
                      type="number"
                      value={parameters.thickness}
                      onChange={(e) => handleParameterChange("thickness", Number(e.target.value))}
                      min="100"
                      max="300"
                      step="25"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="beamSpacing">Beam Spacing (mm)</Label>
                    <Input
                      id="beamSpacing"
                      type="number"
                      value={parameters.beamSpacing}
                      onChange={(e) => handleParameterChange("beamSpacing", Number(e.target.value))}
                      min="400"
                      max="1000"
                      step="100"
                    />
                  </div>
                </div>

                <Separator />

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="beamWidth">Beam Width (mm)</Label>
                    <Input
                      id="beamWidth"
                      type="number"
                      value={parameters.beamWidth}
                      onChange={(e) => handleParameterChange("beamWidth", Number(e.target.value))}
                      min="200"
                      max="500"
                      step="50"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="beamDepth">Beam Depth (mm)</Label>
                    <Input
                      id="beamDepth"
                      type="number"
                      value={parameters.beamDepth}
                      onChange={(e) => handleParameterChange("beamDepth", Number(e.target.value))}
                      min="200"
                      max="500"
                      step="50"
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
                  <Label htmlFor="sunshadeNumber">Drawing Number</Label>
                  <Input
                    id="sunshadeNumber"
                    value={parameters.sunshadeNumber}
                    onChange={(e) => handleParameterChange("sunshadeNumber", e.target.value)}
                    placeholder="SS-001"
                  />
                </div>

                {/* Calculated Values */}
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">Calculated Values</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm text-blue-800">
                    <div>
                      <span className="font-medium">Number of Beams:</span> {numberOfBeams}
                    </div>
                    <div>
                      <span className="font-medium">Type:</span> {getSunshadeTypeTitle()}
                    </div>
                    <div>
                      <span className="font-medium">Area:</span> {((parameters.width * parameters.projection) / 1000000).toFixed(2)} m²
                    </div>
                    <div>
                      <span className="font-medium">Volume:</span> {((parameters.width * parameters.projection * parameters.thickness) / 1000000000).toFixed(3)} m³
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
                  Customize the appearance of your sunshade drawing
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
                      id="showBeams"
                      checked={drawing.showBeams}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showBeams: checked }))}
                    />
                    <Label htmlFor="showBeams">Show Support Beams</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Switch
                      id="showReinforcement"
                      checked={drawing.showReinforcement}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showReinforcement: checked }))}
                    />
                    <Label htmlFor="showReinforcement">Show Reinforcement</Label>
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
                <span>Sunshade Drawing</span>
              </CardTitle>
              <CardDescription>
                Real-time 2D representation of your sunshade design
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
                    <div className="text-muted-foreground">{parameters.sunshadeNumber}</div>
                  </div>
                  <div className="text-center">
                    <div className="font-medium">Type</div>
                    <div className="text-muted-foreground capitalize">{sunshadeType.replace('-', ' ')}</div>
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
