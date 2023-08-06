from typing import Any, List, Type
from zipfile import ZipFile
from UniversalParser._tools import read_content_from_zipobj
import UniversalParser as UP
from ._tools import *

class UPSheet:

    def __init__(self
            , name: str
            , sheetId: str
            , r_id: str
            , zip_obj: ZipFile
            , sheet_path: str
            , sis: List[str]
        ) -> None:

        self.name = name
        self.sheetId = sheetId
        self.r_id = r_id
        self._sis = sis
        
        self.shape = [1, 1] # 维度信息，[行数, 列数]
        self.size = 0 # 元素个数

        content = read_content_from_zipobj(zip_obj, sheet_path)
        self.manager = UP.parse_xml(content, analysis_text=False)

        self._init_shape()
    
    def _init_shape(self):
        dimension = self.manager.find_nodes_by_tag('dimension', one_=True)
        try:
            begin_loc, end_loc = dimension.ref.strip().split(':')
            begin_info = split_char_number(begin_loc)
            end_info = split_char_number(end_loc)
            self.shape[1] = get_width_by_char(begin_info[0], end_info[0])
            self.shape[0] = int(end_info[1]) - int(begin_info[1]) + 1
        except:
            pass

    def get_cell_by_coordinate(self, coordinate: str) -> Any:
        '''根据坐标 'A1'、'B23'等等定位获取单元格的值
        
        如果坐标对应的单元格的值为空，则一致返回 None
        '''
        try:
            cell = self.manager.find_node_by_attrs(r=coordinate)
        except:
            return None
        else:
            v = cell.get('v')
            if v is not None: v=self.manager.find_text(v)
            if 't' in cell and 's' == cell.t:
                v = self._sis[int(v)]
            return v if v else None

    def __getitem__(self, index):
        if isinstance(index, slice):
            if index.step is not None:
                raise TypeError('Unsupport `step` attr.')
            if not (index.start is not None 
                and index.stop is not None
                and isinstance(index.start, str) and C_N_PATT.match(index.start)
                and isinstance(index.stop, str) and C_N_PATT.match(index.stop)):
                raise TypeError('`start` and `stop` must be `str` like `A11`.')
            else:
                begin_ch, begin_num = split_char_number(index.start)
                end_ch, end_num = split_char_number(index.stop)
                begin_num, end_num = int(begin_num), int(end_num)
                width = get_width_by_char(begin_ch, end_ch)
                if not (width>=0
                    and end_num-begin_num>=0):
                    raise TypeError('`stop` must behind and right `start`.')
                else:
                    rows = []
                    for _r in range(begin_num, end_num+1):
                        row = []
                        for _c in range(width):
                            row.append(self.get_cell_by_coordinate(f'{chr(65+_c)}{_r}'))
                        rows.append(row)
                return rows
                
        elif isinstance(index, tuple):
            if 2 == len(index):
                row_index: slice = index[0]
                col_index: slice = index[1]
                # 此处不做错误控制，延用range的语法规则，请参考range的用法
                rows = []
                for _r in range(row_index.start, row_index.stop+1, row_index.step if row_index.step else 1):
                    row = []
                    start = col_index.start
                    end = col_index.stop
                    if isinstance(start, str):
                        start = ord(start) - 65
                    if isinstance(end, str):
                        end = ord(end) - 65 + 1
                    for _c in range(start, end, col_index.step if col_index.step else 1):
                        row.append(self.get_cell_by_coordinate(f'{chr(65+_c)}{_r}'))
                    rows.append(row)
                return rows
            else:
                raise TypeError('Only support two `slice` type.')
        elif isinstance(index, str) and C_N_PATT.match(index):
            return self.get_cell_by_coordinate(index)
        else:
            raise TypeError('index must be `str` like `A1` or `Tuple[slice, slice]` or `clice`.')

    # def __setitem__(self):
    #     ...

    # def __delitem__(self):
    #     ...

    def get_cells_by_range(self, begin_coordinate: str, end_coordinate: str) -> List[Any]:
        '''给定单元格返回，获取一个二维表数据
        '''
        ...

    def get_all_cells(self) -> List[Any]:
        '''获取所有的单元格数据，返回的二维表大小依据shape的大小而定
        '''
        ...

    def modify_cell_by_coordinate(self, coordinate: str):
        pass

    def modify_name(self, new_name: str) -> str:
        pass
