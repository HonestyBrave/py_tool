# !/usr/bin/env python
# -- coding: utf-8 --

# https://blog.csdn.net/SeeTheWorld518/article/details/49535285
# https://blog.csdn.net/weixin_33928137/article/details/93172887
# https://blog.csdn.net/qq280929090/article/details/78859858
# https://blog.csdn.net/weixin_42782150/article/details/106219001
# https://blog.csdn.net/qq_37174526/article/details/89489212
# https://www.cnblogs.com/awakenedy/articles/9303721.html

import os
import xml

from xml.dom import minidom

# ==由于minidom默认的writexml()函数在读取一个xml文件后，修改后重新写入如果加了newl='\n',会将原有的xml中写入多余的行
# ==因此使用下面这个函数来代替
def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    writer.write(indent + "<" + self.tagName)

    attrs = self._get_attributes()
    a_names = attrs.keys()
    # a_names.sort()

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        xml.dom.minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 and self.childNodes[0].nodeType == xml.dom.minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s" % (newl))
        for node in self.childNodes:
            if node.nodeType is not xml.dom.minidom.Node.TEXT_NODE:
                node.writexml(writer, indent + addindent, addindent, newl)
        writer.write("%s</%s>%s" % (indent, self.tagName, newl))
    else:
        writer.write("/>%s" % (newl))

xml.dom.minidom.Element.writexml = fixed_writexml

class Xml():
    def __init__(self, xml_path):
        super(Xml,self).__init__()

        self.xmlPath = xml_path
        self.xmlName = os.path.split(xml_path)[1]

    def createXml(self,root_object,root_attribute_dict,child_value_list_dict):
        doc = xml.dom.minidom.Document()
        #创建一个根节点Managers对象
        root = doc.createElement(root_object)
        # 设置根节点的属性
        for attribute in root_attribute_dict:
            root.setAttribute(attribute, root_attribute_dict[attribute])
        # 将根节点添加到文档对象中
        doc.appendChild(root)

        for child_dict in child_value_list_dict:
            first_node = doc.createElement(child_dict[0])
            for key in child_dict[1]:
                second_node = doc.createElement(key)
                second_node_text = doc.createTextNode(str(child_dict[1][key]))
                second_node.appendChild(second_node_text)
                first_node.appendChild(second_node)
            root.appendChild(first_node)

        # 开始写xml文档
        with open(self.xmlPath, 'w') as file:
            doc.writexml(file, addindent='\t', newl='\n', encoding="utf-8")
        print("create {} success!".format(self.xmlPath))

    def addSecondNodeContent2Xml(self,child_value_list_dict):

        if not os.path.exists(self.xmlPath):
            print("xml not exists!")
            return

        dom_tree = xml.dom.minidom.parse(self.xmlPath)
        root_node = dom_tree.documentElement

        for child_dict in child_value_list_dict:
            first_node = dom_tree.createElement(child_dict[0])
            for key in child_dict[1]:
                second_node = dom_tree.createElement(key)
                second_node_text = dom_tree.createTextNode(str(child_dict[1][key]))
                second_node.appendChild(second_node_text)
                first_node.appendChild(second_node)
            root_node.appendChild(first_node)

        with open(self.xmlPath, 'w') as file:
            dom_tree.writexml(file, addindent='\t', newl='\n', encoding="utf-8")
        print("add first node success!")

    def addThirdNodeContent2Xml(self, need_add_node, add_second_node_value):
        if not os.path.exists(self.xmlPath):
            print("xml not exists!")
            return

        dom_tree = xml.dom.minidom.parse(self.xmlPath)
        root_node = dom_tree.documentElement

        # 获取根节点下所有节点，同样，获取某子节点下所有节点，也是类似，先通过根节点找到子节点，然后找到子节点所有子节点
        all_second_node = root_node.childNodes

        # 遍历所有子节点，找到符合的子节点
        for child_node in all_second_node:
            if child_node.nodeName == str(need_add_node):
                for dict_value in add_second_node_value:
                    for key in dict_value:
                        third_node = dom_tree.createElement(key)
                        third_node_node_text = dom_tree.createTextNode(str(dict_value[key]))
                        third_node.appendChild(third_node_node_text)
                    child_node.appendChild(third_node)

        with open(self.xmlPath, 'w') as file:
            dom_tree.writexml(file, addindent='\t', newl='\n', encoding="utf-8")
        print("add second node success!")

    def modifyNodeValue(self,modify_parent_node,modefy_node_name,modify_value):
        if not os.path.exists(self.xmlPath):
            print("xml not exists!")
            return

        dom_tree = xml.dom.minidom.parse(self.xmlPath)
        root_node = dom_tree.documentElement

        # 获取根节点下所有节点，同样，获取某子节点下所有节点，也是类似，先通过根节点找到子节点，然后找到子节点所有子节点
        all_second_node = root_node.childNodes

        # 遍历所有子节点，找到符合的子节点
        for child_node in all_second_node:
            if child_node.nodeName == str(modify_parent_node):
                child_node.getElementsByTagName(str(modefy_node_name))[0].childNodes[0].nodeValue = modify_value

        with open(self.xmlPath, 'w') as file:
            dom_tree.writexml(file, addindent='\t', newl='\n', encoding="utf-8")
        print("modify node value success!")

    def deleteNode(self,need_delete_node):

        if not os.path.exists(self.xmlPath):
            print("xml not exists!")
            return

        dom_tree = xml.dom.minidom.parse(self.xmlPath)
        root_node = dom_tree.documentElement
        all_second_node = root_node.childNodes
        for child_node in all_second_node:
            if child_node.nodeName == str(need_delete_node):
                root_node.removeChild(child_node)

        with open(self.xmlPath, 'w') as file:
            dom_tree.writexml(file, addindent='\t', newl='\n', encoding="utf-8")
        print("delete node success!")


if __name__ == "__main__":

    xml_path = r"D:\work\test\university.xml"
    root_object = "university"
    root_attribute_dict = {"county":"chine","school":"qinghua"}
    child_value_list_dict = [["xueyuan", {'name': 'jixiyuan', 'createtime': "1900", 'studentnum': 3000}],
                             ["xueyuan", {'name': 'jisuanji', 'createtime': "1930", 'studentnum': 1288}],
                             ["xueyuan", {'name': 'shenmingkexue', 'createtime': "1910", 'studentnum': 2288}]
                            ]

    xml_handle = Xml(xml_path)
    # 创建xml
    xml_handle.createXml(root_object,root_attribute_dict,child_value_list_dict)
    # 增加节点 - 增加第一节点
    child_value_list_dict = [["dangwei", {'name': 'diyidangwei', 'createtime': "1819", 'studentnum': 1000}],
                             ["shitang", {'name': 'haochin', 'createtime': "1369", 'studentnum': 999}],
                             ["jiaoxuelou", {'name': 'diyijiaoxuelou', 'createtime': "1383", 'studentnum': 3133}]
                             ]
    xml_handle.addSecondNodeContent2Xml(child_value_list_dict)
    # 增加节点 - 增加第二节点,在"jiaoxuelou"节点下增加一个 <jiaoxuelounum>1024</jiaoxuelounum> 节点
    add_second_node_value = [{"jiaoxuelounum":1024}]
    need_add_node = "jiaoxuelou"

    xml_handle.addThirdNodeContent2Xml(need_add_node,add_second_node_value)

    modify_parent_node = "dangwei"
    modefy_node_name = "name"
    modify_value = "dangweijigou"
    xml_handle.modifyNodeValue(modify_parent_node,modefy_node_name,modify_value)

    delete_node = "jiaoxuelou"
    xml_handle.deleteNode(delete_node)

