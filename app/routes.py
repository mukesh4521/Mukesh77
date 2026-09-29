from fastapi import (
    APIRouter,
    Request,
    Form,
    HTTPException
)

from fastapi.templating import (
    Jinja2Templates
)

from pydantic import BaseModel

from services.gemini_flash import generate_outline
from services.gemini_pro import generate_story
from services.image_generator import generate_image
from services.layout_builder import build_comic_layout
from services.exporters import save_pdf


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


class PromptRequest(BaseModel):

    prompt: str
    character_name: str
    setting: str
    tone: str
    art_style: str


@router.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


@router.post("/generate")
async def generate_comic(

    request: Request,

    prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...)
):

    try:

        full_prompt = f"""
Story idea: {prompt}

Main character:
{character_name}

Setting:
{setting}

Story tone:
{tone}

Art style:
{art_style}
"""

        # Step 1
        # Generate comic outline

        outline = generate_outline(
            full_prompt
        )

        if not outline:

            raise ValueError(
                "Unable to generate outline"
            )

        # Step 2
        # Generate narration

        full_story = generate_story(
            outline
        )

        # Step 3
        # Generate images

        image_paths = []

        for panel in outline:

            image_prompt = f"""
{panel.get('image_prompt')}

Main character:
{character_name}

Art style:
{art_style}

Comic illustration
"""

            image_path = generate_image(
                image_prompt,
                filename=f"panel_{panel['panel']}.png"
            )

            image_paths.append(
                image_path
            )

        # Step 4
        # Build comic layout

        layout = build_comic_layout(
            image_paths,
            full_story,
            outline
        )

        # Step 5
        # Generate PDF

        pdf_path = save_pdf(
            layout
        )

        browser_pdf_path = (
            "/" +
            pdf_path.replace("\\", "/")
        )

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "request": request,
                "layout": layout,
                "pdf_path":
                    browser_pdf_path
            }
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.post(
    "/generate-comic/json"
)
async def generate_comic_json(
    data: PromptRequest
):

    try:

        full_prompt = f"""
Story idea:
{data.prompt}

Main character:
{data.character_name}

Setting:
{data.setting}

Tone:
{data.tone}

Art style:
{data.art_style}
"""

        outline = generate_outline(
            full_prompt
        )

        story = generate_story(
            outline
        )

        image_paths = []

        for panel in outline:

            image_path = generate_image(

                f"""
{panel['image_prompt']}

Style:
{data.art_style}
""",

                f"panel_{panel['panel']}.png"
            )

            image_paths.append(
                image_path
            )

        layout = build_comic_layout(
            image_paths,
            story,
            outline
        )

        pdf_path = save_pdf(
            layout
        )

        return {

            "success": True,

            "layout": layout,

            "pdf_path":
                "/" +
                pdf_path.replace("\\", "/")
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.get("/export-success")
async def export_success(
    request: Request,
    pdf_path: str = ""
):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "request": request,
            "pdf_path": pdf_path
        }
    )


@router.get("/test-image")
async def test_image():

    try:

        image_path = generate_image(
            "A superhero standing on a mountain at sunset, comic book art"
        )

        return {
            "success": True,
            "image": image_path
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )