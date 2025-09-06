import { useState, useRef, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { 
  Building2, 
  Download, 
  RotateCcw, 
  Eye,
  Share2
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";

interface FootingParameters {
  columnWidth: number;
  columnDepth: number;
  footingWidth: number;
  footingDepth: number;
  scale: number;
  footingNumber: string;
}

interface FootingDrawing {
  width: number;
  height: number;
  scale: number;
  showDimensions: boolean;
  showGrid: boolean;
  showCenterLines: boolean;
}

export default function FootingDesign() {
  const [searchParams] = useSearchParams();
  const footingType = searchParams.get("type") || "rectangular";
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  const [parameters, setParameters] = useState<FootingParameters>({
    columnWidth: 400,
    columnDepth: 400,
    footingWidth: 1200,
    footingDepth: 1200,
    scale: 50,
    footingNumber: "F-001"
  });

  const [drawing, setDrawing] = useState<FootingDrawing>({
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
    drawFooting();
  }, [parameters, drawing]);

  const drawFooting = () => {
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

    // Draw footing outline
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw footing
    ctx.beginPath();
    ctx.rect(offsetX, offsetY, parameters.footingWidth * scale, parameters.footingDepth * scale);
    ctx.fill();
    ctx.stroke();

    // Draw column on top
    ctx.fillStyle = "#e5e7eb";
    ctx.strokeStyle = "#374151";
    ctx.lineWidth = 1;
    
    const columnOffsetX = offsetX + (parameters.footingWidth - parameters.columnWidth) * scale / 2;
    const columnOffsetY = offsetY + (parameters.footingDepth - parameters.columnDepth) * scale / 2;
    
    ctx.beginPath();
    ctx.rect(columnOffsetX, columnOffsetY, parameters.columnWidth * scale, parameters.columnDepth * scale);
    ctx.fill();
    ctx.stroke();

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

    const centerX = offsetX + (parameters.footingWidth * scale) / 2;
    const centerY = offsetY + (parameters.footingDepth * scale) / 2;
    
    // Vertical center line
    ctx.beginPath();
    ctx.moveTo(centerX, offsetY - 20);
    ctx.lineTo(centerX, offsetY + parameters.footingDepth * scale + 20);
    ctx.stroke();
    
    // Horizontal center line
    ctx.beginPath();
    ctx.moveTo(offsetX - 20, centerY);
    ctx.lineTo(offsetX + parameters.footingWidth * scale + 20, centerY);
    ctx.stroke();

    ctx.setLineDash([]);
  };

  const drawDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Footing dimensions
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY - 20);
    ctx.lineTo(offsetX + parameters.footingWidth * scale, offsetY - 20);
    ctx.stroke();
    ctx.fillText(`${parameters.footingWidth} mm`, offsetX + (parameters.footingWidth * scale) / 2, offsetY - 25);

    ctx.beginPath();
    ctx.moveTo(offsetX - 20, offsetY);
    ctx.lineTo(offsetX - 20, offsetY + parameters.footingDepth * scale);
    ctx.stroke();
    ctx.save();
    ctx.translate(offsetX - 25, offsetY + (parameters.footingDepth * scale) / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(`${parameters.footingDepth} mm`, 0, 0);
    ctx.restore();

    // Column dimensions
    const columnOffsetX = offsetX + (parameters.footingWidth - parameters.columnWidth) * scale / 2;
    const columnOffsetY = offsetY + (parameters.footingDepth - parameters.columnDepth) * scale / 2;
    
    ctx.beginPath();
    ctx.moveTo(columnOffsetX, columnOffsetY - 10);
    ctx.lineTo(columnOffsetX + parameters.columnWidth * scale, columnOffsetY - 10);
    ctx.stroke();
    ctx.fillText(`${parameters.columnWidth} mm`, columnOffsetX + (parameters.columnWidth * scale) / 2, columnOffsetY - 15);

    ctx.beginPath();
    ctx.moveTo(columnOffsetX - 10, columnOffsetY);
    ctx.lineTo(columnOffsetX - 10, columnOffsetY + parameters.columnDepth * scale);
    ctx.stroke();
    ctx.save();
    ctx.translate(columnOffsetX - 15, columnOffsetY + (parameters.columnDepth * scale) / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(`${parameters.columnDepth} mm`, 0, 0);
    ctx.restore();
  };

  const drawGrid = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 0.5;
    ctx.setLineDash([2, 2]);

    const gridSize = 100 * scale; // 100mm grid
    
    for (let x = offsetX; x <= offsetX + parameters.footingWidth * scale; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, offsetY);
      ctx.lineTo(x, offsetY + parameters.footingDepth * scale);
      ctx.stroke();
    }
    
    for (let y = offsetY; y <= offsetY + parameters.footingDepth * scale; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(offsetX, y);
      ctx.lineTo(offsetX + parameters.footingWidth * scale, y);
      ctx.stroke();
    }

    ctx.setLineDash([]);
  };

  const handleParameterChange = (key: keyof FootingParameters, value: number | string) => {
    setParameters(prev => ({ ...prev, [key]: value }));
  };

  const resetParameters = () => {
    setParameters({
      columnWidth: 400,
      columnDepth: 400,
      footingWidth: 1200,
      footingDepth: 1200,
      scale: 50,
      footingNumber: "F-001"
    });
  };

  const exportDrawing = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const link = document.createElement("a");
    link.download = `footing-drawing-${parameters.footingNumber}.png`;
    link.href = canvas.toDataURL();
    link.click();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Footing Drawing</h1>
          <p className="text-muted-foreground">
            Generate professional footing drawings with customizable parameters
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
            {/* Column Dimensions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Building2 className="w-5 h-5" />
                  <span>Column Dimensions</span>
                </CardTitle>
                <CardDescription>
                  Set the column dimensions for your footing drawing
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="columnWidth">Column Width (mm)</Label>
                    <Input
                      id="columnWidth"
                      type="number"
                      value={parameters.columnWidth}
                      onChange={(e) => handleParameterChange("columnWidth", Number(e.target.value))}
                      min="200"
                      max="800"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="columnDepth">Column Depth (mm)</Label>
                    <Input
                      id="columnDepth"
                      type="number"
                      value={parameters.columnDepth}
                      onChange={(e) => handleParameterChange("columnDepth", Number(e.target.value))}
                      min="200"
                      max="800"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Footing Dimensions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Building2 className="w-5 h-5" />
                  <span>Footing Dimensions</span>
                </CardTitle>
                <CardDescription>
                  Set the footing dimensions for your drawing
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="footingWidth">Footing Width (mm)</Label>
                    <Input
                      id="footingWidth"
                      type="number"
                      value={parameters.footingWidth}
                      onChange={(e) => handleParameterChange("footingWidth", Number(e.target.value))}
                      min="800"
                      max="2000"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="footingDepth">Footing Depth (mm)</Label>
                    <Input
                      id="footingDepth"
                      type="number"
                      value={parameters.footingDepth}
                      onChange={(e) => handleParameterChange("footingDepth", Number(e.target.value))}
                      min="800"
                      max="2000"
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
                  <Label htmlFor="footingNumber">Drawing Number</Label>
                  <Input
                    id="footingNumber"
                    value={parameters.footingNumber}
                    onChange={(e) => handleParameterChange("footingNumber", e.target.value)}
                    placeholder="F-001"
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
                <span>Footing Drawing</span>
              </CardTitle>
              <CardDescription>
                Real-time 2D representation of your footing
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
                    <div className="text-muted-foreground">{parameters.footingNumber}</div>
                  </div>
                  <div className="text-center">
                    <div className="font-medium">Type</div>
                    <div className="text-muted-foreground capitalize">{footingType}</div>
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
