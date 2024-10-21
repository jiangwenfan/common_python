import pymupdf
from pymupdf import Pixmap, Page, Document


class ParsePDF:
    """
    sample file:
    """

    def __init__(self, file_name: str):
        self.doc: Document = pymupdf.open(file_name)
        self.pages = self.doc.page_count

    def get_catalogue(self) -> list[dict]:
        """
        获取pdf的目录信息,返回中dict

        level: 目录级别,也是目录缩进的空格数
        title: 目录标题
        page_num: 目录页码
        """
        catalogue_info: list[list] = self.doc.get_toc(simple=False)

        res = [
            {"level": item[0], "title": item[1], "page_num": item[2]}
            for item in catalogue_info
        ]

        return res

    def get_top_catalogue(self) -> list[dict]:
        """获取所有第一层目录

                返回:
                    [
                        {
                            "title": "title",
                            "page_start_num": 1, # 页码从1开始
                            "page_end_num": 10  # 页码从10结束
                        }
                    ]

                [
          {
            "title": "Preface",
            "page_start_num": 14,
            "page_end_num": 19
          },
          {
            "title": "Part 1: \nIntroduction",
            "page_start_num": 20,
            "page_end_num": 21
          },
          {
            "title": "Chapter 1: Introducing React",
            "page_start_num": 22,
            "page_end_num": 22
          },
          {
            "title": "Chapter 2: Introducing TypeScript",
            "page_start_num": 56,
            "page_end_num": 55
          },
          {
            "title": "Chapter 3: Setting Up React and TypeScript",
            "page_start_num": 94,
            "page_end_num": 93
          },
          {
            "title": "Chapter 4: Using React Hooks",
            "page_start_num": 126,
            "page_end_num": 125
          },
          {
            "title": "Part 2: \nApp Fundamentals",
            "page_start_num": 164,
            "page_end_num": 165
          },
          {
            "title": "Chapter 5: Approaches to Styling React Frontends",
            "page_start_num": 166,
            "page_end_num": 165
          },
          {
            "title": "Chapter 6: Routing with React Router",
            "page_start_num": 198,
            "page_end_num": 198
          },
          {
            "title": "Chapter 7: Working with Forms",
            "page_start_num": 246,
            "page_end_num": 245
          },
          {
            "title": "Part 3: \nData",
            "page_start_num": 282,
            "page_end_num": 283
          },
          {
            "title": "Chapter 8: State Management",
            "page_start_num": 284,
            "page_end_num": 283
          },
          {
            "title": "Chapter 9: Interacting with RESTful APIs",
            "page_start_num": 314,
            "page_end_num": 313
          },
          {
            "title": "Chapter 10: Interacting with GraphQL APIs",
            "page_start_num": 356,
            "page_end_num": 355
          },
          {
            "title": "Part 4: \nAdvanced React",
            "page_start_num": 394,
            "page_end_num": 395
          },
          {
            "title": "Chapter 11: Reusable Components",
            "page_start_num": 396,
            "page_end_num": 395
          },
          {
            "title": "Chapter 12: Unit Testing with Jest and React Testing Library",
            "page_start_num": 432,
            "page_end_num": 432
          },
          {
            "title": "Index",
            "page_start_num": 462,
            "page_end_num": 470
          },
          {
            "title": "Other Books You May Enjoy",
            "page_start_num": 471,
            "page_end_num": 470
          }
        ]
        """
        first_level = None

        data = self.get_catalogue()
        res = []
        for index, item in enumerate(data):
            if first_level is None:
                first_level = item["level"]

            if item["level"] == first_level:
                next_index = index + 1
                if next_index >= len(data):
                    next_index = len(data) - 1
                next_data = data[next_index]
                res.append(
                    {
                        "title": item["title"],
                        "page_start_num": item["page_num"],
                        "page_end_num": next_data["page_num"] - 1,
                    }
                )
        return res

    def get_cover_image(self) -> bytes:
        """获取封面图片,返回图片的字节数据"""
        page: Page = self.doc[0]

        pix: Pixmap = page.get_pixmap()

        res: bytes = pix.tobytes()
        return res

    def get_page_content(self, page_num: int) -> str:
        """获取指定页的内容"""
        page: Page = self.doc[page_num]

        # 1. 页面信息
        # {'width': 549.0, 'height': 684.0, 'blocks': []}
        page_info: dict = page.get_text("dict")

        # 1.1 页面内容块信息
        page_blocks_info: list[dict] = page_info["blocks"]
        # print(f"\n页面有{len(page_blocks_info)}个块\n")

        for block_info in page_blocks_info:
            # 获取每个块的行信息
            print(f"\n页面有{len(page_blocks_info)}个块\n")

            # 2. 块中全部行信息
            line_info: list[dict] = block_info["lines"]
            # print(f"块有{len(line_info)}行")

            line_res = ""
            for line_item in line_info:
                # 获取每行的文字信息

                # 3. 行中全部文字信息
                spans_info: list[dict] = line_item["spans"]
                # print(f"行有{len(spans_info)}个span文字")

                span_text = ""
                for span_info in spans_info:
                    # 获取每个span文字的信息
                    word = span_info["text"]
                    span_text += word
                # print(span_text)
                # 判断一行是否可以合并。 TODO 如果是代码则不合并，否则合并

                line_res += span_text
            print(line_res)


if __name__ == "__main__":
    pdf = ParsePDF(
        "/Users/evans/Nutstore Files/en_books/Learn React with TypeScript -- Carl Rippon -- Packt Publishing .pdf"
    )
    # import json

    # print(json.dumps(pdf.get_top_catalogue(), indent=2))
    # print(pdf.get_cover_image())

    # with open("/Users/evans/Desktop/cover2.png", "wb") as f:
    #     f.write(pdf.get_cover_image())

    pdf.get_page_content(100)
