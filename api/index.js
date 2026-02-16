// 使用Node.js/JavaScript API端点
// 这样避免Python依赖问题

export default function handler(request, response) {
  const { pathname } = new URL(request.url || '', `http://${request.headers.host}`);
  
  // 处理不同的端点
  if (pathname === '/api' || pathname === '/api/') {
    return response.status(200).json({
      message: 'Welcome to Micro SaaS Scout API',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      endpoints: ['/api/health', '/api/hello', '/api/stats', '/api/docs']
    });
  }
  
  if (pathname === '/api/health') {
    return response.status(200).json({
      status: 'healthy',
      service: 'micro-saas-scout-api',
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'development'
    });
  }
  
  if (pathname === '/api/hello') {
    return response.status(200).json({
      message: 'Hello from Micro SaaS Scout API!',
      timestamp: new Date().toISOString()
    });
  }
  
  if (pathname === '/api/stats') {
    return response.status(200).json({
      timestamp: new Date().toISOString(),
      system: 'Micro SaaS Scout',
      status: 'operational',
      uptime: '100%'
    });
  }
  
  if (pathname === '/api/docs') {
    const html = `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Micro SaaS Scout API Documentation</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 40px; }
          h1 { color: #333; }
          .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
          .method { background: #4CAF50; color: white; padding: 5px 10px; border-radius: 3px; }
          .url { font-family: monospace; color: #0066cc; }
        </style>
      </head>
      <body>
        <h1>📚 API Documentation</h1>
        <p>Simple REST API for Micro SaaS Scout project.</p>
        
        <div class="endpoint">
          <span class="method">GET</span> <span class="url">/api/</span>
          <p>API root endpoint</p>
        </div>
        
        <div class="endpoint">
          <span class="method">GET</span> <span class="url">/api/health</span>
          <p>Health check endpoint</p>
        </div>
        
        <div class="endpoint">
          <span class="method">GET</span> <span class="url">/api/hello</span>
          <p>Hello test endpoint</p>
        </div>
        
        <div class="endpoint">
          <span class="method">GET</span> <span class="url">/api/stats</span>
          <p>System statistics</p>
        </div>
        
        <h2>Testing</h2>
        <pre>
curl https://micro-saas-scout.vercel.app/api/
curl https://micro-saas-scout.vercel.app/api/health
curl https://micro-saas-scout.vercel.app/api/hello
        </pre>
      </body>
      </html>
    `;
    
    return response
      .status(200)
      .setHeader('Content-Type', 'text/html')
      .send(html);
  }
  
  // 404处理
  return response.status(404).json({
    error: 'Not Found',
    message: `Endpoint ${pathname} not found`,
    timestamp: new Date().toISOString(),
    availableEndpoints: ['/api/', '/api/health', '/api/hello', '/api/stats', '/api/docs']
  });
}