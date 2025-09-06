import { useState } from "react";
import { Download, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { exportDrawing, ExportOptions } from "@/utils/exportUtils";

interface ExportDropdownProps {
  canvas: HTMLCanvasElement | null;
  filename: string;
  title?: string;
  author?: string;
  subject?: string;
  keywords?: string[];
  onExportStart?: () => void;
  onExportComplete?: () => void;
}

const exportFormats = [
  { value: 'png', label: 'PNG Image', description: 'High-quality raster image' },
  { value: 'pdf', label: 'PDF Document', description: 'Professional PDF with metadata' },
  { value: 'svg', label: 'SVG Vector', description: 'Scalable vector graphics' },
  { value: 'dxf', label: 'DXF File', description: 'AutoCAD compatible format' },
  { value: 'dwg', label: 'DWG File', description: 'AutoCAD native format (DXF fallback)' },
] as const;

export default function ExportDropdown({
  canvas,
  filename,
  title,
  author,
  subject,
  keywords,
  onExportStart,
  onExportComplete
}: ExportDropdownProps) {
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async (format: typeof exportFormats[number]['value']) => {
    if (!canvas) {
      alert('No drawing available to export');
      return;
    }

    try {
      setIsExporting(true);
      onExportStart?.();

      const options: ExportOptions = {
        filename,
        title,
        author,
        subject,
        keywords
      };

      await exportDrawing(canvas, format, options);
      
      // Show success message
      const formatLabel = exportFormats.find(f => f.value === format)?.label;
      console.log(`Successfully exported as ${formatLabel}`);
      
    } catch (error) {
      console.error('Export failed:', error);
      alert(`Failed to export as ${format.toUpperCase()}. Please try again.`);
    } finally {
      setIsExporting(false);
      onExportComplete?.();
    }
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button 
          variant="outline" 
          disabled={!canvas || isExporting}
          className="min-w-[140px]"
        >
          <Download className="w-4 h-4 mr-2" />
          {isExporting ? 'Exporting...' : 'Export'}
          <ChevronDown className="w-4 h-4 ml-2" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56">
        {exportFormats.map((format) => (
          <DropdownMenuItem
            key={format.value}
            onClick={() => handleExport(format.value)}
            disabled={isExporting}
            className="flex flex-col items-start p-3 cursor-pointer hover:bg-gray-50"
          >
            <div className="font-medium">{format.label}</div>
            <div className="text-sm text-gray-500">{format.description}</div>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
