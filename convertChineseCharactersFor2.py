#-*- coding: utf-8 -*-
import sublime, sublime_plugin
import sys
import re
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf8")
    from HTMLParser import HTMLParser
    parser = HTMLParser()
    PY = 2;
if sys.version[0] == '3':
    PY = 3;

class ChineseCharactersToUnicodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        fileName = self.view.file_name()
        fileSuffix = re.match(r'.+\.(\w+)$',fileName).group(1)
        if fileSuffix == "js" or fileSuffix == "json" or fileSuffix == "css":  
            def TU(x):
                if fileSuffix == "js" or fileSuffix == "json":
                    return '\\u'+('000'+hex(ord(x))[2:])[-4:]
                else:
                    return '\\'+('000'+hex(ord(x))[2:])[-4:]  
            def toUnicode(x):
                s = x.group(0)
                s = list(s)
                mapValue = map(TU,s)
                s = "".join(mapValue)
                return s
            regions = self.view.sel()
            if not regions[0].empty():
                for region in regions:
                    if not region.empty():
                        s = self.view.substr(region)
                        s = re.sub(ur"([\u4e00-\u9fa5]+)",toUnicode,s.decode('utf8'))
                        self.view.replace(edit, region, s)
            else:
                region = sublime.Region(0, self.view.size())
                s = self.view.substr(region)
                s = re.sub(ur"([\u4e00-\u9fa5]+)",toUnicode,s.decode('utf8'))
                
                self.view.replace(edit, region, s)
        else:
            sublime.error_message('不能解析的文件类型')
            
class UnicodeToChineseCharactersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        fileName = self.view.file_name()
        fileSuffix = re.match(r'.+\.(\w+)$',fileName).group(1)
        if fileSuffix == "js" or fileSuffix == "json" or fileSuffix == "css":
            def unicodeTo(x):
                s = x.group(0)
                if fileSuffix == "js" or fileSuffix == "json":
                    s = s[2:]
                else:
                    s = s[1:]
                if PY == 2:
                    s = parser.unescape('&#'+str(int(s,16))+';')
                elif PY == 3:
                    s = chr(int(s,16))
                else:
                    sublime.error_message('解析失败')
                return s
            regions = self.view.sel()
            if not regions[0].empty():
                for region in regions:
                    if not region.empty():
                        s = self.view.substr(region)
                        if fileSuffix == "js" or fileSuffix == "json":
                            s = re.sub(r"(\\[uU]\w{4})",unicodeTo,s)
                        else:
                            s = re.sub(r"(\\\w{4})",unicodeTo,s)
                        self.view.replace(edit, region, s)
            else:
                region = sublime.Region(0, self.view.size())
                s = self.view.substr(region)
                if fileSuffix == "js" or fileSuffix == "json":
                    s = re.sub(r"(\\[uU]\w{4})",unicodeTo,s)
                else:
                    s = re.sub(r"(\\\w{4})",unicodeTo,s)
                self.view.replace(edit, region, s)
        else:
            sublime.error_message('不能解析的文件类型')