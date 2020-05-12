class inkycal_layout:
  """Page layout handling"""

  def __init__(self, model=None, width=None, height=None,
               supports_colour=False):
    """Initialize parameters for specified epaper model
    Use model parameter to specify display OR
    Crate a custom display with given width and height"""

    self.background_colour = 'white' # Move to inkycal_rendering
    self.text_colour = 'black'       # Move to inkycal_rendering

    if (model != None) and (width == None) and (height == None):
      display_dimensions = {
      'epd_7_in_5_v2_colour': (800, 400),
      'epd_7_in_5_v2': (800, 400),
      'epd_7_in_5_colour': (640, 384),
      'epd_7_in_5': (640, 384),
      'epd_5_in_83_colour': (600, 448),
      'epd_5_in_83': (600, 448),
      'epd_4_in_2_colour': (400, 300),
      'epd_4_in_2': (400, 300),
      }

      self.display_height, self.display_width = display_dimensions[model]
      if 'colour' in model:
        self.three_colour_support = True

    elif width and height:
      self.display_height = width
      self.display_width = height
      self.supports_colour = supports_colour

    else:
      print("Can't create a layout without given sizes")
      raise

    self.__top_section_width = self.display_width
    self.__middle_section_width = self.display_width
    self.__bottom_section_width = self.display_width
    self.create_sections()

  def create_sections(self, top_section=0.10, middle_section=0.65,
                      bottom_section=0.25):
    """Allocate fixed percentage height for top and middle section
    e.g. 0.2 = 20% (Leave empty for default values)
    Set top/bottom_section to 0 to allocate more space for the middle section
    """
    scale = lambda percentage: round(percentage * self.display_height)

    if top_section == 0 or bottom_section == 0:
      if top_section == 0:
        self.__top_section_height = 0

      if bottom_section == 0:
        self.__bottom_section_height = 0

      self.__middle_section_height = scale(1 - top_section - bottom_section)
    else:
      if top_section + middle_section + bottom_section > 1.0:
        print('All percentages should add up to max 100%, not more!')
        raise

      self.__top_section_height = scale(top_section)
      self.__middle_section_height = scale(middle_section)
      self.__bottom_section_height = (self.display_height -
        self.__top_section_height - self.__middle_section_height)

  def get_section_size(self, section):
    """Enter top/middle/bottom to get the size of the section as a tuple:
    (width, height)"""
    if section not in ['top','middle','bottom']:
      print('Invalid section: ', section)
      raise
    else:
      if section == 'top':
        size = (self.__top_section_width, self.__top_section_height)
      elif section == 'middle':
        size = (self.__middle_section_width, self.__middle_section_height)
      elif section == 'bottom':
        size = (self.__bottom_section_width, self.__bottom_section_height)
      return size