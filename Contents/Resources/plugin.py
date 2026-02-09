# encoding: utf-8

###########################################################################################################
#
# General Plugin
#
# Read the docs:
# https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
import math
from GlyphsApp import Glyphs, EDIT_MENU, GSNode, GSGuideLine
from GlyphsApp.plugins import GeneralPlugin
from AppKit import NSMenuItem, NSAlert, NSEventModifierFlagCommand, NSEventModifierFlagOption, NSEventModifierFlagControl


class EnhancedCenterGuideline(GeneralPlugin):

    @objc.python_method
    def settings(self):
        """
        Plugin name localization shown in the Glyphs UI.
        """
        self.name = Glyphs.localize({
            'en': 'Enhanced Center Guideline',
            'hu': 'Továbbfejlesztett segédvonal középvezetéshez',
            'de': 'Verbesserte Mittellinienführung',
            'fr': 'Guide de centre amélioré',
            'es': 'Guía central mejorada',
            'pt': 'Guia central aprimorada',
            'zh': '增强型中心辅助线'
        })

    @objc.python_method
    def start(self):
        """
        Creates a new menu item in the Edit menu with shortcut:
        Command + Option + Control + G
        """
        newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.name, self.showWindow_, "g")
        newMenuItem.setTarget_(self)
        newMenuItem.setKeyEquivalentModifierMask_(NSEventModifierFlagCommand | NSEventModifierFlagOption | NSEventModifierFlagControl)
        Glyphs.menu[EDIT_MENU].append(newMenuItem)

    def showWindow_(self, sender):
        """
        Main execution function.
        Runs when the menu item or shortcut is triggered.
        """
        activeFont = Glyphs.font
        if not activeFont or not activeFont.selectedLayers:
            return
        
        activeLayer = activeFont.selectedLayers[0]

        # --- Helper functions ---

        def chooseOrientation():
            """
            Shows an alert dialog to let the user choose
            the orientation of the new guideline.
            Returns a string identifier or None if Cancel is pressed.
            """
            alert = NSAlert.alloc().init()
            alert.setMessageText_("Guideline Orientation")
            alert.setInformativeText_("Select the orientation for the new guideline:")
            alert.addButtonWithTitle_("Horizontal")             # 1000
            alert.addButtonWithTitle_("Vertical")               # 1001
            alert.addButtonWithTitle_("Diagonal (perpendicular)")       # 1002
            alert.addButtonWithTitle_("Diagonal (between lines)")       # 1003
            alert.addButtonWithTitle_("Cancel")                 # 1004

            response = alert.runModal()

            if response == 1000: return "horizontal"
            elif response == 1001: return "vertical"
            elif response == 1002: return "diagonal_perpendicular"
            elif response == 1003: return "diagonal_between_lines"
            elif response == 1004: return None  # Cancel → exit plugin logic

        def calculate_line_angle(nodes):
            """
            Calculates the angle of the line defined
            by the first and last selected node.
            """
            if len(nodes) < 2: return 0
            dx = nodes[-1].position.x - nodes[0].position.x
            dy = nodes[-1].position.y - nodes[0].position.y
            return math.degrees(math.atan2(dy, dx)) % 180

        def calculate_midpoint(nodes):
            """
            Calculates the average (center) position of selected nodes.
            """
            if not nodes: return (0, 0)
            return (
                sum([n.position.x for n in nodes]) / len(nodes),
                sum([n.position.y for n in nodes]) / len(nodes)
            )

        # --- Main execution logic ---

        selected_nodes = [n for n in activeLayer.selection if isinstance(n, GSNode)]
        selected_guides = [g for g in activeLayer.selection if isinstance(g, GSGuideLine)]
        
        # Continue only if at least two elements are selected
        if (len(selected_nodes) + len(selected_guides)) >= 2:
            orientation = chooseOrientation()
            if not orientation:
                return  # Cancel pressed → exit

            newGuide = GSGuideLine()
            mid_pos = (0, 0)
            angle = 0

            # --- Case 1: One node + one guide ---
            if len(selected_nodes) == 1 and len(selected_guides) == 1:
                g, n = selected_guides[0], selected_nodes[0]
                mid_pos = ((n.position.x + g.position.x)/2, (n.position.y + g.position.y)/2)

                if orientation == "horizontal":
                    mid_pos, angle = (n.position.x, (n.position.y + g.position.y)/2), 0
                elif orientation == "vertical":
                    mid_pos, angle = ((n.position.x + g.position.x)/2, n.position.y), 90
                elif orientation == "diagonal_between_lines":
                    angle = g.angle
                else:
                    angle = (g.angle + 90) % 180

            # --- Case 2: Two guides selected ---
            elif len(selected_guides) == 2:
                g1, g2 = selected_guides[0], selected_guides[1]
                mid_pos = ((g1.position.x + g2.position.x)/2, (g1.position.y + g2.position.y)/2)

                if orientation == "horizontal":
                    angle = 0
                elif orientation == "vertical":
                    angle = 90
                elif orientation == "diagonal_between_lines":
                    angle = (g1.angle + g2.angle) / 2
                else:
                    angle = ((g1.angle + g2.angle) / 2 + 90) % 180

            # --- Case 3: Only nodes selected (at least two) ---
            else:
                mid_pos = calculate_midpoint(selected_nodes)

                if orientation == "horizontal":
                    angle = 0
                elif orientation == "vertical":
                    angle = 90
                elif orientation == "diagonal_perpendicular":
                    angle = (calculate_line_angle(selected_nodes) + 90) % 180
                else:  # diagonal_between_lines
                    if len(selected_nodes) >= 4:
                        # Compute angle between two averaged node pairs
                        x_sorted = sorted(selected_nodes, key=lambda n: n.position.x)
                        dx = (
                            (x_sorted[-1].position.x + x_sorted[-2].position.x) / 2
                            - (x_sorted[0].position.x + x_sorted[1].position.x) / 2
                        )
                        dy = (
                            (x_sorted[-1].position.y + x_sorted[-2].position.y) / 2
                            - (x_sorted[0].position.y + x_sorted[1].position.y) / 2
                        )
                        angle = math.degrees(math.atan2(dy, dx)) % 180
                    else:
                        angle = calculate_line_angle(selected_nodes)

            # Apply position and angle, then add the new guideline
            newGuide.position = mid_pos
            newGuide.angle = angle
            activeLayer.guides.append(newGuide)

    @objc.python_method
    def __file__(self):
        """
        Required by Glyphs plugin system.
        Do not modify.
        """
        return __file__
