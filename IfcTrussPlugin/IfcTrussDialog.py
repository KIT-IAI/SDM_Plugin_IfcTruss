# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class IfcTrussDialog
###########################################################################

class IfcTrussDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"IfcTruss Results", pos = wx.DefaultPosition, size = wx.Size( 411,333 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_grid = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_grid.CreateGrid( 0, 0 )
		self.m_grid.EnableEditing( False )
		self.m_grid.EnableGridLines( True )
		self.m_grid.EnableDragGridSize( False )
		self.m_grid.SetMargins( 0, 0 )

		# Columns
		self.m_grid.AutoSizeColumns()
		self.m_grid.EnableDragColMove( False )
		self.m_grid.EnableDragColSize( True )
		self.m_grid.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_grid.EnableDragRowSize( True )
		self.m_grid.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer1.Add( self.m_grid, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_buttonOk = wx.Button( self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonOk.SetDefault()
		bSizer1.Add( self.m_buttonOk, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


