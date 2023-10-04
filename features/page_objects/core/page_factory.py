import sys
import importlib


class PageFactory:
    @staticmethod
    def get_page_object(page_name, driver, platform):


        module_name = f"features.page_objects.{platform}.{page_name}_page"

        try:

            module = importlib.import_module(module_name)


            page_class = getattr(module, page_name.capitalize() + "Page")


            return page_class(driver, platform)
        except (ImportError, AttributeError):
            sys.stderr.write(f"Erreur : Impossible d'importer {module_name} ou la classe n'existe pas.\n")
            return None
