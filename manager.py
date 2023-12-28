import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'falcon.settings')
    try:
        print("Hello World")
    except ImportError as exc:
        raise ImportError(
            "Coun't import Django"
        )

if __name__ == '__main__':
    main()