import { serve } from "https://deno.land/std@0.140.0/http/server.ts";

async function handleRequest(request: Request): Promise<Response> {
  const { pathname } = new URL(request.url);
  if (pathname.startsWith("/indigenous-mountain.jpeg")) {
    const file = await Deno.readFile("./indigenous-mountain.jpeg");
    return new Response(file, {
      headers: {
        "content-type": "image/jpeg",
      },
    });
  }
  return new Response(
    `<!DOCTYPE html>
     <html>
       <head>
         <meta charset="UTF-8">
         <meta name="viewport" content="width=device.width, initial-scale=1.0">
         <title>Free Ararat</title>
       </head>
       <body>
         <img src="indigenous-mountain.jpeg"
              alt="Protestors advocating for recognition of the cultural significance of Mount Ararat to the Armenian people" />
       </body>
     </html>`,
    {
      headers: {
        "content-type": "text/html; charset=UTF-8",
      },
    },
  );
}

serve(handleRequest);
