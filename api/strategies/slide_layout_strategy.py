from abc import ABC, abstractmethod
from pptx.util import Inches
from api.strategies.creative_asset_strategy import SingleAsset, MultipleAssets


class SlideLayout(ABC):
    def __init__(self, presentation: object, post_data: dict) -> None:
        self.presentation = presentation
        self.post_data = post_data
        self.platform: str = post_data["platform"]
        self.account: str = post_data["account"]
        self.country: str = post_data["country"]
        self.audience: str = post_data["audience"]
        #! paid headline won't always be available in post data
        #! self.paid_headline = post_data["paid_headline"]
        self.social_copy: str = post_data["copy"]
        self.link: str = post_data["link"]

    def create_blank_slide(self) -> None:
        """Create blank power point slide.

        Selects a slide layout from avoialable power point options and
        adds a new slide with that layout to the passed instance of
        :param:presenation.

        The `Presentation` instance is inherited from base class `SlideLayout`.

        :return: returns slide object
        :rtype: `object`
        """

        blank_slide_layout = self.presentation.slide_layouts[6]
        detail_slide = self.presentation.slides.add_slide(blank_slide_layout)
        self.detail_slide = detail_slide

    def create_platform_textbox(self) -> None:
        """Create a textbox for a social platform."""
        # Text box positioning and size definitions
        left = Inches(0.25)
        top = Inches(0.25)
        width = Inches(4.5)
        height = Inches(0.4)
        # Textbox setup and adding text
        slide = self.detail_slide
        platform_tbox = slide.shapes.add_textbox(left, top, width, height)
        platform_tf = platform_tbox.text_frame
        # Adding bold text and normal text in single paragraph with runs
        p = platform_tf.paragraphs[0]
        # Bold run
        bold_run = p.add_run()
        bold_run.text = "Platform: "
        bold_run_font = bold_run.font
        bold_run_font.bold = True
        # Normal run
        normal_run = p.add_run()
        normal_run.text = self.platform

    def create_country_textbox(self) -> None:
        """Create textbox foor country."""
        # Text box positioning and size definitions
        left = Inches(5.25)
        top = Inches(0.25)
        width = Inches(4.39)
        height = Inches(0.4)
        # Textbox setup
        slide = self.detail_slide
        account_tbox = slide.shapes.add_textbox(left, top, width, height)
        account_tf = account_tbox.text_frame
        # Adding bold text and normal text in single paragraph with runs
        p = account_tf.paragraphs[0]
        # Bold run
        bold_run = p.add_run()
        bold_run.text = "Country: "
        bold_run_font = bold_run.font
        bold_run_font.bold = True
        # Normal run
        normal_run = p.add_run()
        normal_run.text = self.country

    def create_account_textbox(self) -> None:
        """Create a textbox for a social account."""
        # Text box positioning and size definitions
        left = Inches(0.25)
        top = Inches(0.75)
        width = Inches(4.5)
        height = Inches(0.4)
        # Textbox setup
        slide = self.detail_slide
        account_tbox = slide.shapes.add_textbox(left, top, width, height)
        account_tf = account_tbox.text_frame
        # Adding bold text and normal text in single paragraph with runs
        p = account_tf.paragraphs[0]
        # Bold run
        bold_run = p.add_run()
        bold_run.text = "Account: "
        bold_run_font = bold_run.font
        bold_run_font.bold = True
        # Normal run
        normal_run = p.add_run()
        normal_run.text = self.account

    def create_audience_textbox(self) -> None:
        """Create textbox foor country."""
        # Text box positioning and size definitions
        left = Inches(5.25)
        top = Inches(0.75)
        width = Inches(4.39)
        height = Inches(0.4)
        # Textbox setup
        slide = self.detail_slide
        account_tbox = slide.shapes.add_textbox(left, top, width, height)
        account_tf = account_tbox.text_frame
        # Adding bold text and normal text in single paragraph with runs
        p = account_tf.paragraphs[0]
        # Bold run
        bold_run = p.add_run()
        bold_run.text = "Audience: "
        bold_run_font = bold_run.font
        bold_run_font.bold = True
        # Normal run
        normal_run = p.add_run()
        normal_run.text = self.audience

    # needs to be abstract method - position changes based on layout strategy
    # @abstractmethod
    def create_social_copy_textbox(self) -> None:
        """Create textbox for social copy."""
        # Text box positioning and size definitions
        left = Inches(0.25)
        top = Inches(1.65)
        width = Inches(4.5)
        height = Inches(4.64)
        # Textbox setup
        slide = self.detail_slide
        account_tbox = slide.shapes.add_textbox(left, top, width, height)
        account_tf = account_tbox.text_frame
        account_tf.word_wrap = True
        # Adding bold text and normal text in separate paragraphs
        p1 = account_tf.paragraphs[0]
        # Bold paragraph
        run = p1.add_run()
        run.text = "Copy:\n"
        font = run.font
        font.bold = True
        # Normal paragraph
        p2 = account_tf.add_paragraph()
        p2.text = self.social_copy

    def create_link_textbox(self) -> None:
        """Create textbox for link."""
        # Text box positioning and size definitions
        left = Inches(5.25)
        top = Inches(1.65)
        width = Inches(4.39)
        height = Inches(0.4)
        # Textbox setup
        slide = self.detail_slide
        account_tbox = slide.shapes.add_textbox(left, top, width, height)
        account_tf = account_tbox.text_frame
        # Adding bold text and normal text in single paragraph with runs
        p = account_tf.paragraphs[0]
        # Bold run
        bold_run = p.add_run()
        bold_run.text = "Link: "
        bold_run_font = bold_run.font
        bold_run_font.bold = True
        # Normal run
        # todo: if there is no link, don't add a hyperlink address
        normal_run = p.add_run()
        normal_run.text = self.link
        hyperlink = normal_run.hyperlink
        hyperlink.address = self.link

    # need abstract methods later if adding creative assets differs for organic and paid layouts
    # these are currently implemented in the same way, irrespective of layout type - no abstract method decorator needed
    def add_creative_assets(self) -> None:

        # use creative asset strategy here
        if "creative" in self.post_data.keys():
            creative_asset_data: list = self.post_data["creative"]
            creative_asset_count = len(creative_asset_data)
            if creative_asset_count == 1:
                creative_strategy = SingleAsset(self.detail_slide, creative_asset_data)
                creative_strategy.build_asset_layout()

            elif (creative_asset_count > 1) and (creative_asset_count <= 12):
                # for asset in creative_asset_data:
                #     asset_counter = 1
                # InsertMultipleAssets(self.detail_slide, asset)
                pass
            else:
                # handle outlier cases here - maybe with error when number of creative assets exceeds 12
                pass
        else:
            # logic for posts with no creative asset
            pass


class Organic(SlideLayout):
    """Strategy for creating organic post slide layout.

    Organic option for slide layouts. This format omits values that exist in other type of posts such as paid promotions. For example, this layout does not include a `paid_headline`.
    """

    # todo: implement build layout method
    def build_layout(self):
        # create blank slide
        self.create_blank_slide()
        # create all textboxes
        self.create_platform_textbox()
        self.create_country_textbox()
        self.create_account_textbox()
        self.create_audience_textbox()
        self.create_social_copy_textbox()
        self.create_link_textbox()
        # todo: add paid/organic type and tentative publish date textboxes here
        # add creative asset
        self.add_creative_assets()


# class Paid(SlideLayout):
#     """Strategy for creating paid post slide layout."""

#     # need to explicitly implement init here to add the paid_headline property
#     def __init__(self) -> None:
#         # inherit init values from base class
#         super().__init__()
#         # set paid headline - we know it exists at this point
#         self.paid_headline: str = self.post_data["paid_headline"]

#     # new paid headline copy section - social copy moved down to accomodate
#     def create_paid_headline_textbox(self) -> None:
#         pass

#     def create_social_copy_textbox(self) -> None:
#         pass
