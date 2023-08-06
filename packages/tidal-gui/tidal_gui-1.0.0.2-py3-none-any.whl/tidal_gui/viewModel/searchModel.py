#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  searchModel.py
@Date    :  2021/8/17
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import _thread
import threading

import aigpy.stringHelper
import tidal_dl
from PyQt5.QtCore import pyqtSignal
from aigpy.modelHelper import ModelBase
from tidal_dl import Type
from tidal_dl.model import Album, SearchResult

from tidal_gui.tidalImp import tidalImp
from tidal_gui.view.searchView import SearchView
from tidal_gui.viewModel.viewModel import ViewModel


class SearchModel(ViewModel):
    SIGNAL_ADD_TASKITEM = pyqtSignal(ModelBase)

    def __init__(self):
        super(SearchModel, self).__init__()
        self._lock = threading.Lock()
        self._resultData = SearchResult()
        
        self.view = SearchView()
        self.view.setPageIndex(1, 1)
        self.view.connectButton('search', self.__search__)
        self.view.connectButton('prePage', self.__searchPre__)
        self.view.connectButton('nextPage', self.__searchNext__)
        self.view.connectButton('download', self.__download__)
        self.view.connectTab(self.__search__)

    def __getSumByResult__(self, stype: Type):
        if stype == Type.Album:
            return self._resultData.albums.totalNumberOfItems
        elif stype == Type.Artist:
            return self._resultData.artists.totalNumberOfItems
        elif stype == Type.Track:
            return self._resultData.tracks.totalNumberOfItems
        elif stype == Type.Video:
            return self._resultData.videos.totalNumberOfItems
        elif stype == Type.Playlist:
            return self._resultData.playlists.totalNumberOfItems
        return 0
    
    
    def __startThread__(self, index: int):
        def __thread_search__(model: SearchModel, index: int):
            typeIndex = model.view.getSelectedTabIndex()
            # pageIndex = model.view.getPageIndex()
            searchText = model.view.getSearchText()

            if aigpy.stringHelper.isNull(searchText):
                # errmessage
                model._lock.release()
                return
            
            # search
            limit = 20
            offset = (index - 1) * limit
            stype = tidal_dl.Type(typeIndex)
            msg, model._resultData = tidalImp.search(searchText, stype, offset, limit)

            if not aigpy.stringHelper.isNull(msg):
                # errmessage
                model._lock.release()
                return

            # set page index
            total = model.__getSumByResult__(stype)
            maxIdx = total // limit + (1 if total % limit > 0 else 0)
            if index > maxIdx:
                model._lock.release()
                return
            model.view.setPageIndex(index, maxIdx)

            # set table
            model.view.setTableItems(stype, offset, model._resultData)
            model._lock.release()

        _thread.start_new_thread(__thread_search__, (self, index))



    def __search__(self, num: int = 0):
        if not self._lock.acquire(False):
            return
        
        index = 1
        if num != 0:
            curIdx, curSum = self.view.getPageIndex()
            if curIdx + num > 1:
                index = curIdx + num
        
        self.__startThread__(index)

    def __searchNext__(self):
        self.__search__(1)

    def __searchPre__(self):
        self.__search__(-1)


    def __download__(self):
        typeIndex = self.view.getSelectedTabIndex()
        stype = tidal_dl.Type(typeIndex)
        index = self.view.getSelectedTableIndex(stype)
        if index <= 0:
            pass

        data = None
        if stype == Type.Album:
            data = self._resultData.albums.items[index]
        elif stype == Type.Track:
            data = self._resultData.tracks.items[index]
        elif stype == Type.Video:
            data = self._resultData.videos.items[index]
        elif stype == Type.Playlist:
            data = self._resultData.playlists.items[index]

        if data is not None:
            self.SIGNAL_ADD_TASKITEM.emit(data)
