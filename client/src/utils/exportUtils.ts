import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export interface ExportOptions {
  filename: string;
  title?: string;
  author?: string;
  subject?: string;
  keywords?: string[];
}

// Export canvas as PNG
export const exportAsPNG = (canvas: HTMLCanvasElement, options: ExportOptions): void => {
  const link = document.createElement("a");
  link.download = `${options.filename}.png`;
  link.href = canvas.toDataURL("image/png");
  link.click();
};

// Export canvas as PDF
export const exportAsPDF = async (canvas: HTMLCanvasElement, options: ExportOptions): Promise<void> => {
  try {
    // Create PDF document
    const pdf = new jsPDF({
      orientation: 'landscape',
      unit: 'mm',
      format: 'a4'
    });

    // Add metadata
    if (options.title) pdf.setProperties({ title: options.title });
    if (options.author) pdf.setProperties({ author: options.author });
    if (options.subject) pdf.setProperties({ subject: options.subject });
    if (options.keywords) pdf.setProperties({ keywords: options.keywords.join(', ') });

    // Convert canvas to image data
    const imgData = canvas.toDataURL('image/png');
    
    // Calculate dimensions to fit in PDF
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = pdf.internal.pageSize.getHeight();
    
    // Calculate aspect ratio
    const canvasAspectRatio = canvas.width / canvas.height;
    const pdfAspectRatio = pdfWidth / pdfHeight;
    
    let imgWidth, imgHeight;
    if (canvasAspectRatio > pdfAspectRatio) {
      // Canvas is wider, fit to width
      imgWidth = pdfWidth - 20; // 10mm margin on each side
      imgHeight = imgWidth / canvasAspectRatio;
    } else {
      // Canvas is taller, fit to height
      imgHeight = pdfHeight - 20; // 10mm margin on each side
      imgWidth = imgHeight * canvasAspectRatio;
    }

    // Center the image
    const x = (pdfWidth - imgWidth) / 2;
    const y = (pdfHeight - imgHeight) / 2;

    // Add title
    pdf.setFontSize(16);
    pdf.setFont('helvetica', 'bold');
    pdf.text(options.title || 'Drawing', pdfWidth / 2, 15, { align: 'center' });

    // Add drawing
    pdf.addImage(imgData, 'PNG', x, y + 10, imgWidth, imgHeight);

    // Add footer with timestamp
    pdf.setFontSize(10);
    pdf.setFont('helvetica', 'normal');
    const timestamp = new Date().toLocaleString();
    pdf.text(`Generated on: ${timestamp}`, 10, pdfHeight - 10);

    // Save PDF
    pdf.save(`${options.filename}.pdf`);
  } catch (error) {
    console.error('Error exporting PDF:', error);
    alert('Error exporting PDF. Please try again.');
  }
};

// Export canvas as SVG (closest to DWG format we can achieve in browser)
export const exportAsSVG = (canvas: HTMLCanvasElement, options: ExportOptions): void => {
  try {
    // Convert canvas to SVG-like structure
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Create SVG content
    const svgContent = `
      <svg width="${canvas.width}" height="${canvas.height}" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <style>
            .drawing-element { stroke: #000; stroke-width: 1; fill: none; }
            .text-element { font-family: Arial, sans-serif; font-size: 12px; fill: #000; }
          </style>
        </defs>
        <rect width="100%" height="100%" fill="white"/>
        <image href="${canvas.toDataURL()}" width="100%" height="100%"/>
      </svg>
    `;

    // Create blob and download
    const blob = new Blob([svgContent], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${options.filename}.svg`;
    link.click();
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error exporting SVG:', error);
    alert('Error exporting SVG. Please try again.');
  }
};

// Export canvas as DXF (AutoCAD compatible format)
export const exportAsDXF = (canvas: HTMLCanvasElement, options: ExportOptions): void => {
  try {
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Basic DXF header
    let dxfContent = `0
SECTION
2
HEADER
9
$ACADVER
1
AC1014
9
$DWGCODEPAGE
3
ANSI_1252
9
$INSBASE
10
0.0
20
0.0
30
0.0
9
$EXTMIN
10
0.0
20
0.0
30
0.0
9
$EXTMAX
10
${canvas.width}
20
${canvas.height}
30
0.0
9
$LIMMIN
10
0.0
20
0.0
9
$LIMMAX
10
${canvas.width}
20
${canvas.height}
0
ENDSEC
0
SECTION
2
ENTITIES
`;

    // Convert canvas to base64 for embedding
    const imgData = canvas.toDataURL('image/png');
    
    // Add image entity (simplified representation)
    dxfContent += `0
IMAGE
8
0
10
0.0
20
0.0
30
0.0
11
${canvas.width}
21
${canvas.height}
31
0.0
340
0
`;

    // Close DXF
    dxfContent += `0
ENDSEC
0
EOF`;

    // Create blob and download
    const blob = new Blob([dxfContent], { type: 'application/dxf' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${options.filename}.dxf`;
    link.click();
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Error exporting DXF:', error);
    alert('Error exporting DXF. Please try again.');
  }
};

// Export canvas as DWG (using a library that can generate DWG files)
export const exportAsDWG = async (canvas: HTMLCanvasElement, options: ExportOptions): Promise<void> => {
  try {
    // For now, we'll export as DXF which is AutoCAD compatible
    // In a production environment, you might want to use a specialized DWG library
    exportAsDXF(canvas, options);
    
    // Note: True DWG export requires specialized libraries like:
    // - AutoCAD API (server-side)
    // - ODA File Converter SDK
    // - LibreDWG (open source)
    
    console.log('DWG export not available in browser. Exported as DXF instead.');
  } catch (error) {
    console.error('Error exporting DWG:', error);
    alert('Error exporting DWG. Please try again.');
  }
};

// Export drawing with multiple format options
export const exportDrawing = async (
  canvas: HTMLCanvasElement, 
  format: 'png' | 'pdf' | 'svg' | 'dxf' | 'dwg',
  options: ExportOptions
): Promise<void> => {
  switch (format) {
    case 'png':
      exportAsPNG(canvas, options);
      break;
    case 'pdf':
      await exportAsPDF(canvas, options);
      break;
    case 'svg':
      exportAsSVG(canvas, options);
      break;
    case 'dxf':
      exportAsDXF(canvas, options);
      break;
    case 'dwg':
      await exportAsDWG(canvas, options);
      break;
    default:
      throw new Error(`Unsupported format: ${format}`);
  }
};
