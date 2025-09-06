import { useState, useRef, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import {
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

interface BridgeParameters {
  spanLength: number;
  deckWidth: number;
  deckThickness: number;
  pierHeight: number;
  pierWidth: number;
  abutmentHeight: number;
  abutmentWidth: number;
  scale: number;
  bridgeNumber: string;
}

interface BridgeDrawing {
  width: number;
  height: number;
  scale: number;
  showDimensions: boolean;
  showGrid: boolean;
  showCenterLines: boolean;
  showReinforcement: boolean;
}

export default function BridgeDesign() {
  const [searchParams] = useSearchParams();
  const bridgeType = searchParams.get("type") || "beam";
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const [parameters, setParameters] = useState<BridgeParameters>({
    spanLength: 20000,
    deckWidth: 8000,
    deckThickness: 400,
    pierHeight: 5000,
    pierWidth: 1200,
    abutmentHeight: 3000,
    abutmentWidth: 2000,
    scale: 50,
    bridgeNumber: "B-001"
  });

  const [drawing, setDrawing] = useState<BridgeDrawing>({
    width: 1200,
    height: 800,
    scale: 50,
    showDimensions: true,
    showGrid: false,
    showCenterLines: true,
    showReinforcement: false
  });

  const [activeTab, setActiveTab] = useState("drawing");

  // Update drawing when parameters change
  useEffect(() => {
    drawBridge();
  }, [parameters, drawing]);

  const drawBridge = () => {
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

    if (bridgeType === "beam") {
      drawBeamBridge(ctx, offsetX, offsetY, scale);
    } else if (bridgeType === "arch") {
      drawArchBridge(ctx, offsetX, offsetY, scale);
    } else if (bridgeType === "cable") {
      drawCableBridge(ctx, offsetX, offsetY, scale);
    } else if (bridgeType === "truss") {
      drawTrussBridge(ctx, offsetX, offsetY, scale);
    }

    // Draw grid if enabled
    if (drawing.showGrid) {
      drawGrid(ctx, offsetX, offsetY, scale);
    }
  };

  const drawBeamBridge = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw deck
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, parameters.spanLength * scale, parameters.deckWidth * scale);
    ctx.fill();
    ctx.stroke();

    // Draw piers
    const pierCount = 3; // 2 abutments + 1 pier
    const pierSpacing = parameters.spanLength * scale / (pierCount - 1);
    
    for (let i = 0; i < pierCount; i++) {
      const pierX = offsetX + i * pierSpacing;
      const pierY = offsetY + 200 + parameters.deckWidth * scale;
      
      ctx.fillStyle = "#6b7280";
      ctx.beginPath();
      ctx.rect(pierX - (parameters.pierWidth * scale) / 2, pierY, parameters.pierWidth * scale, parameters.pierHeight * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw abutments
    ctx.fillStyle = "#374151";
    ctx.beginPath();
    ctx.rect(offsetX - parameters.abutmentWidth * scale / 2, offsetY + 200 + parameters.deckWidth * scale + parameters.pierHeight * scale, parameters.abutmentWidth * scale, parameters.abutmentHeight * scale);
    ctx.fill();
    ctx.stroke();
    
    ctx.beginPath();
    ctx.rect(offsetX + parameters.spanLength * scale - parameters.abutmentWidth * scale / 2, offsetY + 200 + parameters.deckWidth * scale + parameters.pierHeight * scale, parameters.abutmentWidth * scale, parameters.abutmentHeight * scale);
    ctx.fill();
    ctx.stroke();

    // Draw reinforcement if enabled
    if (drawing.showReinforcement) {
      drawBridgeReinforcement(ctx, offsetX, offsetY, scale);
    }

    // Draw center lines if enabled
    if (drawing.showCenterLines) {
      drawBridgeCenterLines(ctx, offsetX, offsetY, scale);
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawBeamBridgeDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawArchBridge = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw arch
    const archCenterX = offsetX + (parameters.spanLength * scale) / 2;
    const archCenterY = offsetY + 200 + parameters.deckWidth * scale;
    const archRadius = parameters.spanLength * scale / 2;
    
    ctx.beginPath();
    ctx.arc(archCenterX, archCenterY, archRadius, 0, Math.PI, true);
    ctx.stroke();

    // Draw deck
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, parameters.spanLength * scale, parameters.deckWidth * scale);
    ctx.fill();
    ctx.stroke();

    // Draw piers
    const pierCount = 3;
    const pierSpacing = parameters.spanLength * scale / (pierCount - 1);
    
    for (let i = 0; i < pierCount; i++) {
      const pierX = offsetX + i * pierSpacing;
      const pierY = offsetY + 200 + parameters.deckWidth * scale;
      
      ctx.fillStyle = "#6b7280";
      ctx.beginPath();
      ctx.rect(pierX - (parameters.pierWidth * scale) / 2, pierY, parameters.pierWidth * scale, parameters.pierHeight * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw abutments
    ctx.fillStyle = "#374151";
    ctx.beginPath();
    ctx.rect(offsetX - parameters.abutmentWidth * scale / 2, offsetY + 200 + parameters.deckWidth * scale + parameters.pierHeight * scale, parameters.abutmentWidth * scale, parameters.abutmentHeight * scale);
    ctx.fill();
    ctx.stroke();
    
    ctx.beginPath();
    ctx.rect(offsetX + parameters.spanLength * scale - parameters.abutmentWidth * scale / 2, offsetY + 200 + parameters.deckWidth * scale + parameters.pierHeight * scale, parameters.abutmentWidth * scale, parameters.abutmentHeight * scale);
    ctx.fill();
    ctx.stroke();

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawArchBridgeDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawCableBridge = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw towers
    const towerHeight = parameters.pierHeight * 1.5;
    const towerWidth = parameters.pierWidth * 1.2;
    
    // Left tower
    ctx.fillStyle = "#374151";
    ctx.beginPath();
    ctx.rect(offsetX - towerWidth * scale / 2, offsetY + 200, towerWidth * scale, towerHeight * scale);
    ctx.fill();
    ctx.stroke();
    
    // Right tower
    ctx.beginPath();
    ctx.rect(offsetX + parameters.spanLength * scale - towerWidth * scale / 2, offsetY + 200, towerWidth * scale, towerHeight * scale);
    ctx.fill();
    ctx.stroke();

    // Draw deck
    ctx.fillStyle = "#f3f4f6";
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200 + towerHeight * scale, parameters.spanLength * scale, parameters.deckWidth * scale);
    ctx.fill();
    ctx.stroke();

    // Draw cables
    ctx.strokeStyle = "#6b7280";
    ctx.lineWidth = 1;
    const cableCount = 8;
    const cableSpacing = parameters.spanLength * scale / (cableCount - 1);
    
    for (let i = 0; i < cableCount; i++) {
      const cableX = offsetX + i * cableSpacing;
      const cableStartY = offsetY + 200 + towerHeight * scale / 2;
      const cableEndY = offsetY + 200 + towerHeight * scale + parameters.deckWidth * scale;
      
      ctx.beginPath();
      ctx.moveTo(cableX, cableStartY);
      ctx.lineTo(cableX, cableEndY);
      ctx.stroke();
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawCableBridgeDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawTrussBridge = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#1f2937";
    ctx.lineWidth = 2;
    ctx.fillStyle = "#f3f4f6";

    // Draw deck
    ctx.beginPath();
    ctx.rect(offsetX, offsetY + 200, parameters.spanLength * scale, parameters.deckWidth * scale);
    ctx.fill();
    ctx.stroke();

    // Draw truss structure
    ctx.strokeStyle = "#6b7280";
    ctx.lineWidth = 1;
    
    const trussHeight = parameters.deckWidth * scale * 0.8;
    const trussSpacing = parameters.spanLength * scale / 8;
    
    // Draw top chord
    for (let i = 0; i <= 8; i++) {
      const x = offsetX + i * trussSpacing;
      const y = offsetY + 200 - trussHeight;
      
      if (i > 0) {
        ctx.beginPath();
        ctx.moveTo(x - trussSpacing, y);
        ctx.lineTo(x, y);
        ctx.stroke();
      }
    }
    
    // Draw bottom chord
    for (let i = 0; i <= 8; i++) {
      const x = offsetX + i * trussSpacing;
      const y = offsetY + 200 + parameters.deckWidth * scale;
      
      if (i > 0) {
        ctx.beginPath();
        ctx.moveTo(x - trussSpacing, y);
        ctx.lineTo(x, y);
        ctx.stroke();
      }
    }
    
    // Draw vertical members
    for (let i = 0; i <= 8; i++) {
      const x = offsetX + i * trussSpacing;
      const topY = offsetY + 200 - trussHeight;
      const bottomY = offsetY + 200 + parameters.deckWidth * scale;
      
      ctx.beginPath();
      ctx.moveTo(x, topY);
      ctx.lineTo(x, bottomY);
      ctx.stroke();
    }
    
    // Draw diagonal members
    for (let i = 0; i < 8; i++) {
      const x1 = offsetX + i * trussSpacing;
      const x2 = offsetX + (i + 1) * trussSpacing;
      const topY = offsetY + 200 - trussHeight;
      const bottomY = offsetY + 200 + parameters.deckWidth * scale;
      
      // Left diagonal
      ctx.beginPath();
      ctx.moveTo(x1, topY);
      ctx.lineTo(x2, bottomY);
      ctx.stroke();
      
      // Right diagonal
      ctx.beginPath();
      ctx.moveTo(x1, bottomY);
      ctx.lineTo(x2, topY);
      ctx.stroke();
    }

    // Draw piers
    const pierCount = 3;
    const pierSpacing = parameters.spanLength * scale / (pierCount - 1);
    
    for (let i = 0; i < pierCount; i++) {
      const pierX = offsetX + i * pierSpacing;
      const pierY = offsetY + 200 + parameters.deckWidth * scale;
      
      ctx.fillStyle = "#6b7280";
      ctx.beginPath();
      ctx.rect(pierX - (parameters.pierWidth * scale) / 2, pierY, parameters.pierWidth * scale, parameters.pierHeight * scale);
      ctx.fill();
      ctx.stroke();
    }

    // Draw dimensions if enabled
    if (drawing.showDimensions) {
      drawTrussBridgeDimensions(ctx, offsetX, offsetY, scale);
    }
  };

  const drawBridgeReinforcement = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);

    // Draw deck reinforcement
    const barSpacing = 500 * scale;
    for (let x = offsetX; x <= offsetX + parameters.spanLength * scale; x += barSpacing) {
      ctx.beginPath();
      ctx.moveTo(x, offsetY + 200);
      ctx.lineTo(x, offsetY + 200 + parameters.deckWidth * scale);
      ctx.stroke();
    }

    for (let y = offsetY + 200; y <= offsetY + 200 + parameters.deckWidth * scale; y += barSpacing) {
      ctx.beginPath();
      ctx.moveTo(offsetX, y);
      ctx.lineTo(offsetX + parameters.spanLength * scale, y);
      ctx.stroke();
    }

    ctx.setLineDash([]);
  };

  const drawBridgeCenterLines = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#dc2626";
    ctx.lineWidth = 1;
    ctx.setLineDash([10, 5]);

    // Vertical center line
    const centerX = offsetX + (parameters.spanLength * scale) / 2;
    ctx.beginPath();
    ctx.moveTo(centerX, offsetY + 200 - 100);
    ctx.lineTo(centerX, offsetY + 200 + parameters.deckWidth * scale + parameters.pierHeight * scale + parameters.abutmentHeight * scale + 100);
    ctx.stroke();

    // Horizontal center line
    const centerY = offsetY + 200 + (parameters.deckWidth * scale) / 2;
    ctx.beginPath();
    ctx.moveTo(offsetX - 100, centerY);
    ctx.lineTo(offsetX + parameters.spanLength * scale + 100, centerY);
    ctx.stroke();

    ctx.setLineDash([]);
  };

  const drawBeamBridgeDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Span length
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY + 150);
    ctx.lineTo(offsetX + parameters.spanLength * scale, offsetY + 150);
    ctx.stroke();
    ctx.fillText(`${parameters.spanLength / 1000} m`, offsetX + (parameters.spanLength * scale) / 2, offsetY + 140);

    // Deck width
    ctx.beginPath();
    ctx.moveTo(offsetX - 30, offsetY + 200);
    ctx.lineTo(offsetX - 30, offsetY + 200 + parameters.deckWidth * scale);
    ctx.stroke();
    ctx.save();
    ctx.translate(offsetX - 35, offsetY + 200 + (parameters.deckWidth * scale) / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText(`${parameters.deckWidth} mm`, 0, 0);
    ctx.restore();
  };

  const drawArchBridgeDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Span: ${parameters.spanLength / 1000} m`, offsetX + 400, offsetY + 150);
    ctx.fillText(`Width: ${parameters.deckWidth} mm`, offsetX + 400, offsetY + 165);
    ctx.fillText(`Type: Arch Bridge`, offsetX + 400, offsetY + 180);
  };

  const drawCableBridgeDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Span: ${parameters.spanLength / 1000} m`, offsetX + 400, offsetY + 150);
    ctx.fillText(`Width: ${parameters.deckWidth} mm`, offsetX + 400, offsetY + 165);
    ctx.fillText(`Type: Cable-Stayed Bridge`, offsetX + 400, offsetY + 180);
  };

  const drawTrussBridgeDimensions = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.fillStyle = "#374151";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";

    // Basic dimensions
    ctx.fillText(`Span: ${parameters.spanLength / 1000} m`, offsetX + 400, offsetY + 150);
    ctx.fillText(`Width: ${parameters.deckWidth} mm`, offsetX + 400, offsetY + 165);
    ctx.fillText(`Type: Truss Bridge`, offsetX + 400, offsetY + 180);
  };

  const drawGrid = (ctx: CanvasRenderingContext2D, offsetX: number, offsetY: number, scale: number) => {
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 0.5;
    ctx.setLineDash([2, 2]);

    const gridSize = 1000 * scale; // 1m grid
    const maxWidth = Math.max(parameters.spanLength * scale, 1000);
    const maxHeight = 1000;

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

  const handleParameterChange = (key: keyof BridgeParameters, value: number | string) => {
    setParameters(prev => ({ ...prev, [key]: value }));
  };

  const resetParameters = () => {
    setParameters({
      spanLength: 20000,
      deckWidth: 8000,
      deckThickness: 400,
      pierHeight: 5000,
      pierWidth: 1200,
      abutmentHeight: 3000,
      abutmentWidth: 2000,
      scale: 50,
      bridgeNumber: "B-001"
    });
  };

  const getExportOptions = () => ({
    filename: `bridge-drawing-${parameters.bridgeNumber}`,
    title: `${getBridgeTypeTitle()} - ${parameters.bridgeNumber}`,
    author: "LISP Canvas",
    subject: "Bridge Design Drawing",
    keywords: ["bridge", "design", "drawing", "construction", "engineering"]
  });

  const getBridgeTypeTitle = () => {
    switch (bridgeType) {
      case "beam": return "Beam Bridge";
      case "arch": return "Arch Bridge";
      case "cable": return "Cable-Stayed Bridge";
      case "truss": return "Truss Bridge";
      default: return "Bridge Design";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{getBridgeTypeTitle()}</h1>
          <p className="text-muted-foreground">
            Generate professional bridge drawings with customizable parameters
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={resetParameters}>
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
          <ExportDropdown
            canvas={canvasRef.current}
            filename={`bridge-drawing-${parameters.bridgeNumber}`}
            title={`${getBridgeTypeTitle()} - ${parameters.bridgeNumber}`}
            author="LISP Canvas"
            subject="Bridge Design Drawing"
            keywords={["bridge", "design", "drawing", "construction", "engineering"]}
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
            {/* Bridge Dimensions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Building2 className="w-5 h-5" />
                  <span>Bridge Dimensions</span>
                </CardTitle>
                <CardDescription>
                  Set the geometric parameters for your bridge drawing
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="spanLength">Span Length (mm)</Label>
                    <Input
                      id="spanLength"
                      type="number"
                      value={parameters.spanLength}
                      onChange={(e) => handleParameterChange("spanLength", Number(e.target.value))}
                      min="10000"
                      max="100000"
                      step="1000"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="deckWidth">Deck Width (mm)</Label>
                    <Input
                      id="deckWidth"
                      type="number"
                      value={parameters.deckWidth}
                      onChange={(e) => handleParameterChange("deckWidth", Number(e.target.value))}
                      min="5000"
                      max="15000"
                      step="500"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="deckThickness">Deck Thickness (mm)</Label>
                    <Input
                      id="deckThickness"
                      type="number"
                      value={parameters.deckThickness}
                      onChange={(e) => handleParameterChange("deckThickness", Number(e.target.value))}
                      min="200"
                      max="800"
                      step="50"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="pierHeight">Pier Height (mm)</Label>
                    <Input
                      id="pierHeight"
                      type="number"
                      value={parameters.pierHeight}
                      onChange={(e) => handleParameterChange("pierHeight", Number(e.target.value))}
                      min="2000"
                      max="15000"
                      step="500"
                    />
                  </div>
                </div>

                <Separator />

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="pierWidth">Pier Width (mm)</Label>
                    <Input
                      id="pierWidth"
                      type="number"
                      value={parameters.pierWidth}
                      onChange={(e) => handleParameterChange("pierWidth", Number(e.target.value))}
                      min="800"
                      max="3000"
                      step="100"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="abutmentHeight">Abutment Height (mm)</Label>
                    <Input
                      id="abutmentHeight"
                      type="number"
                      value={parameters.abutmentHeight}
                      onChange={(e) => handleParameterChange("abutmentHeight", Number(e.target.value))}
                      min="1500"
                      max="8000"
                      step="500"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="abutmentWidth">Abutment Width (mm)</Label>
                    <Input
                      id="abutmentWidth"
                      type="number"
                      value={parameters.abutmentWidth}
                      onChange={(e) => handleParameterChange("abutmentWidth", Number(e.target.value))}
                      min="1000"
                      max="5000"
                      step="200"
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
                  <Label htmlFor="bridgeNumber">Drawing Number</Label>
                  <Input
                    id="bridgeNumber"
                    value={parameters.bridgeNumber}
                    onChange={(e) => handleParameterChange("bridgeNumber", e.target.value)}
                    placeholder="B-001"
                  />
                </div>

                {/* Calculated Values */}
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-blue-900 mb-2">Calculated Values</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm text-blue-800">
                    <div>
                      <span className="font-medium">Type:</span> {getBridgeTypeTitle()}
                    </div>
                    <div>
                      <span className="font-medium">Span:</span> {(parameters.spanLength / 1000).toFixed(1)} m
                    </div>
                    <div>
                      <span className="font-medium">Deck Area:</span> {((parameters.spanLength * parameters.deckWidth) / 1000000).toFixed(1)} m²
                    </div>
                    <div>
                      <span className="font-medium">Deck Volume:</span> {((parameters.spanLength * parameters.deckWidth * parameters.deckThickness) / 1000000000).toFixed(2)} m³
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
                  Customize the appearance of your bridge drawing
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
                    min="1000"
                    max="1600"
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
                    min="800"
                    max="1200"
                    step="100"
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
                <span>Bridge Drawing</span>
              </CardTitle>
              <CardDescription>
                Real-time 2D representation of your bridge design
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
                    <div className="text-muted-foreground">{parameters.bridgeNumber}</div>
                  </div>
                  <div className="text-center">
                    <div className="font-medium">Type</div>
                    <div className="text-muted-foreground capitalize">{bridgeType.replace('-', ' ')}</div>
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
