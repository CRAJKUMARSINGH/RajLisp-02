import { useState, useRef, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { 
  Building2, 
  RotateCcw, 
  Eye,
  Share2,
  Circle,
  Square
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import ExportDropdown from "@/components/ExportDropdown";

interface ColumnParameters {
  width: number;
  depth: number;
  diameter: number; // For circular columns
  scale: number;
  columnNumber: string;
}

interface ColumnDrawing {
  width: number;
  height: number;
  scale: number;
  showDimensions: boolean;
  showGrid: boolean;
  showCenterLines: boolean;
}

export default function ColumnDesign() {
  const [searchParams] = useSearchParams();
  const columnType = searchParams.get("type") || "rectangular";
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  const [parameters, setParameters] = useState<ColumnParameters>({
    width: 400,
    depth: 400,
    diameter: 400,
    scale: 50,
    columnNumber: "C-001"
  });

  const [drawing, setDrawing] = useState<ColumnDrawing>({
    width: 800,
    height: 600,
    scale: 50,
    showDimensions: true,
    showGrid: false,
    showCenterLines: true
  });

  const [activeTab, setActiveTab] = useState("drawing");

  // Update drawing when parameters change
  useEffect(() => {
    drawColumn();
  }, [parameters, drawing]);

  const drawColumn = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Set drawing scale
    const scale = drawing.scale / 1000; // Convert mm to meters
    const offsetX = 150;
    const offsetY = 100;

    // Draw column outline
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    if (columnType === "circular") {
      // Circular column
      const radius = (parameters.diameter * scale) / 2;
      const centerX = offsetX + radius;
      const centerY = offsetY + radius;
      
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
      ctx.fill();
      ctx.stroke();
    } else {
      // Rectangular column
      ctx.beginPath();
      ctx.rect(offsetX, offsetY, parameters.width * scale, parameters.depth * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw center lines if enabled
    if (drawing.showCenterLines) {
      drawCenterLines(ctx, offsetX, offsetY, scale);
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawDimensions(ctx, offsetX, offsetY, scale);
    }

    // Draw grid if enabled
    if (drawing.showGrid) {
      drawGrid(ctx, offsetX, offsetY, scale);
    }
  };

  const drawCenterLines = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 1;
    ctx.setLineDash([10, 5]);

    if (columnType === "circular") {
      const radius = (parameters.diameter * scale) / 2;
      const centerX = offsetX + radius;
      const centerY = offsetY + radius;
      
      // Vertical center line
      ctx.beginPath();
      ctx.moveTo(centerX, offsetY - 20);
      ctx.lineTo(centerX, offsetY + parameters.depth * scale + 20);
      ctx.stroke();
      
      // Horizontal center line
      ctx.beginPath();
      ctx.moveTo(offsetX - 20, centerY);
      ctx.lineTo(offsetX + parameters.diameter * scale + 20, centerY);
      ctx.stroke();
    } else {
      const centerX = offsetX + (parameters.width * scale) / 2;
      const centerY = offsetY + (parameters.depth * scale) / 2;
      
      // Vertical center line
      ctx.beginPath();
      ctx.moveTo(centerX, offsetY - 20);
      ctx.lineTo(centerX, offsetY + parameters.depth * scale + 20);
      ctx.stroke();
      
      // Horizontal center line
      ctx.beginPath();
      ctx.moveTo(offsetX - 20, centerY);
      ctx.lineTo(offsetX + parameters.width * scale + 20, centerY);
      ctx.stroke();
    }

    ctx.setLineDash([]);
  };

  const drawDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    if (columnType === "circular") {
      // Diameter dimension
      ctx.beginPath();
      ctx.moveTo(offsetX, offsetY - 20);
      ctx.lineTo(offsetX + parameters.diameter * scale, offsetY - 20);
      ctx.stroke();
      ctx.fillText(`${parameters.diameter} mm`, offsetX + (parameters.diameter * scale) / 2, offsetY - 25);

      // Height dimension
      ctx.beginPath();
      ctx.moveTo(offsetX - 20, offsetY);
      ctx.lineTo(offsetX - 20, offsetY + parameters.depth * scale);
      ctx.stroke();
      ctx.save();
      ctx.translate(offsetX - 25, offsetY + (parameters.depth * scale) / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText(`${parameters.depth} mm`, 0, 0);
      ctx.restore();
    } else {
      // Width dimension
      ctx.beginPath();
      ctx.moveTo(offsetX, offsetY - 20);
      ctx.lineTo(offsetX + parameters.width * scale, offsetY - 20);
      ctx.stroke();
      ctx.fillText(`${parameters.width} mm`, offsetX + (parameters.width * scale) / 2, offsetY - 25);

      // Height dimension
      ctx.beginPath();
      ctx.moveTo(offsetX - 20, offsetY);
      ctx.lineTo(offsetX - 20, offsetY + parameters.depth * scale);
      ctx.stroke();
      ctx.save();
      ctx.translate(offsetX - 25, offsetY + (parameters.depth * scale) / 2);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText(`${parameters.depth} mm`, 0, 0);
      ctx.restore();
    }
  };

  const drawGrid = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 0.5;
    ctx.setLineDash([2, 2]);

    const gridSize = 50 * scale; // 50mm grid

    if (columnType === "circular") {
      const maxDimension = Math.max(parameters.diameter, parameters.depth);
      const gridExtent = Math.ceil(maxDimension / 50) * gridSize;
      
      for (let x = offsetX; x <= offsetX + gridExtent; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, offsetY);
        ctx.lineTo(x, offsetY + gridExtent);
        ctx.stroke();
      }
      
      for (let y = offsetY; y <= offsetY + gridExtent; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(offsetX, y);
        ctx.lineTo(offsetX + gridExtent, y);
        ctx.stroke();
      }
    } else {
      for (let x = offsetX; x <= offsetX + parameters.width * scale; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, offsetY);
        ctx.lineTo(x, offsetY + parameters.depth * scale);
        ctx.stroke();
      }
      
      for (let y = offsetY; y <= offsetY + parameters.depth * scale; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(offsetX, y);
        ctx.lineTo(offsetX + parameters.width * scale, y);
        ctx.stroke();
      }
    }

    ctx.setLineDash([]);
  };

  const handleParameterChange = (key: keyof ColumnParameters, value: number | string) => {
    setParameters(prev => ({ ...prev, [key]: value }));
  };

  const resetParameters = () => {
    setParameters({
      width: 400,
      depth: 400,
      diameter: 400,
      scale: 50,
      columnNumber: "C-001"
    });
  };

  const getExportOptions = () => ({
    filename: `column-drawing-${parameters.columnNumber}`,
    title: `${getColumnTypeTitle()} - ${parameters.columnNumber}`,
    author: "LISP Canvas",
    subject: "Column Design Drawing",
    keywords: ["column", "design", "drawing", "construction", "architecture"]
  });

  const getColumnTypeTitle = () => {
    return columnType === "circular" ? "Circular Column Drawing" : "Rectangular Column Drawing";
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{getColumnTypeTitle()}</h1>
          <p className="text-muted-foreground">
            Generate professional column drawings with customizable parameters
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={resetParameters}>
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
          <ExportDropdown
            canvas={canvasRef.current}
            filename={`column-drawing-${parameters.columnNumber}`}
            title={`${getColumnTypeTitle()} - ${parameters.columnNumber}`}
            author="LISP Canvas"
            subject="Column Design Drawing"
            keywords={["column", "design", "drawing", "construction", "architecture"]}
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
            {/* Column Dimensions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Building2 className="w-5 h-5" />
                  <span>Column Dimensions</span>
                </CardTitle>
                <CardDescription>
                  Set the geometric parameters for your column drawing
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {columnType === "circular" ? (
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="diameter">Diameter (mm)</Label>
                      <Input
                        id="diameter"
                        type="number"
                        value={parameters.diameter}
                        onChange={(e) => handleParameterChange("diameter", Number(e.target.value))}
                        min="200"
                        max="1000"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="depth">Height (mm)</Label>
                      <Input
                        id="depth"
                        type="number"
                        value={parameters.depth}
                        onChange={(e) => handleParameterChange("depth", Number(e.target.value))}
                        min="2000"
                        max="10000"
                      />
                    </div>
                  </div>
                ) : (
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="width">Width (mm)</Label>
                      <Input
                        id="width"
                        type="number"
                        value={parameters.width}
                        onChange={(e) => handleParameterChange("width", Number(e.target.value))}
                        min="200"
                        max="800"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="depth">Depth (mm)</Label>
                      <Input
                        id="depth"
                        type="number"
                        value={parameters.depth}
                        onChange={(e) => handleParameterChange("depth", Number(e.target.value))}
                        min="200"
                        max="800"
                      />
                    </div>
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

                <div className="space-y-2">
                  <Label htmlFor="columnNumber">Drawing Number</Label>
                  <Input
                    id="columnNumber"
                    value={parameters.columnNumber}
                    onChange={(e) => handleParameterChange("columnNumber", e.target.value)}
                    placeholder="C-001"
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
                  Customize the appearance of your drawing
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
                      id="showCenterLines"
                      checked={drawing.showCenterLines}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showCenterLines: checked }))}
                    />
                    <Label htmlFor="showCenterLines">Show Center Lines</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Switch
                      id="showGrid"
                      checked={drawing.showGrid}
                      onCheckedChange={(checked) => setDrawing(prev => ({ ...prev, showGrid: checked }))}
                    />
                    <Label htmlFor="showGrid">Show Grid</Label>
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
                    min="400"
                    max="1200"
                    step="50"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="canvasHeight">Canvas Height (px)</Label>
                  <Input
                    id="canvasHeight"
                    type="number"
                    value={drawing.height}
                    onChange={(e) => setDrawing(prev => ({ ...prev, height: Number(e.target.value) }))}
                    min="300"
                    max="900"
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
                <span>Column Drawing</span>
              </CardTitle>
              <CardDescription>
                Real-time 2D representation of your column
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
                    <div className="text-muted-foreground">{parameters.columnNumber}</div>
                  </div>
                  <div className="text-center">
                    <div className="font-medium">Type</div>
                    <div className="text-muted-foreground capitalize">{columnType}</div>
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
