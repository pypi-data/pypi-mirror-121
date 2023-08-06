#!/usr/bin/env python3
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    try:
        from AFAT.fibrosis import main
        main()
        input('Press Enter to continue ...')
    except Exception as e:
        import traceback
        import sys
        traceback.print_exc(file=sys.stdout)
        print(e)
        input('Press Enter to continue ...')
