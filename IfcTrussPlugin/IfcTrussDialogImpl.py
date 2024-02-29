import IfcTrussDialog
import pandas as pd
import wx

class IfcTrussDialogImpl(IfcTrussDialog.IfcTrussDialog):

    def __init__(self, parent):

        IfcTrussDialog.IfcTrussDialog.__init__(self, parent)

        self.m_grid.SetRowLabelSize(0)
        self.m_grid.SetColLabelSize(0)

    def __del__(self):
        pass

    def fillGrid(self, results):

        resultsDict = results._asdict()

        self.m_grid.AppendCols()

        for key in resultsDict:

            col = 0

            self.m_grid.AppendRows()
            row = self.m_grid.GetNumberRows() - 1

            self.m_grid.SetCellValue(row, col, key)
            self.m_grid.SetCellBackgroundColour(row, col, wx.Colour(0x6B, 0x90, 0x80))
            self.m_grid.SetCellTextColour(row, col, wx.Colour(255, 255, 255))

            value = resultsDict[key]

            if isinstance(value, pd.DataFrame):

                self.m_grid.AppendRows()
                row = self.m_grid.GetNumberRows() - 1

                self.m_grid.SetCellBackgroundColour(row, 0, wx.Colour(0x6B, 0x90, 0x80))

                dataFrameDict = value.to_dict()

                createRows = True

                for key in dataFrameDict:

                    col += 1

                    if len(dataFrameDict) >= self.m_grid.GetNumberCols():
                        self.m_grid.AppendCols()

                    self.m_grid.SetCellBackgroundColour(row-1, col, wx.Colour(0x6B, 0x90, 0x80))
                    self.m_grid.SetCellValue(row, col, key)
                    self.m_grid.SetCellBackgroundColour(row, col, wx.Colour(0xCC, 0xE3, 0xDE))
                    self.m_grid.SetCellTextColour(row, col, wx.Colour(0, 0, 0))

                    values = dataFrameDict[key]

                    if createRows:
                        self.m_grid.AppendRows(len(values))
                        self.m_grid.SetCellBackgroundColour(row+1, 0, wx.Colour(0x6B, 0x90, 0x80))
                        createRows = False

                    valueRow = row + 1

                    for value in values:
                        self.m_grid.SetCellBackgroundColour(valueRow, 0, wx.Colour(0x6B, 0x90, 0x80))
                        self.m_grid.SetCellValue(valueRow, col, str(values[value]))

                        valueRow += 1

            else:
                col += 1
                self.m_grid.SetCellValue(row, col, str(value))

        self.m_grid.AutoSizeColumns
