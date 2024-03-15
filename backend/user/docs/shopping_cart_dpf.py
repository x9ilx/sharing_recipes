import datetime as dt

from reportlab.platypus import Paragraph, Spacer, Table, flowables

from core.base_pdf_classes import BaseDocPortraitTemplate, BaseDocsPDF


class ShoppingCartDocGeneratePDF(BaseDocsPDF):
    def __init__(self, buffer, current_user):
        self.current_user = current_user
        super().__init__(buffer)

    def get_pdf(self):
        doc = BaseDocPortraitTemplate(self.buffer)
        elements = []
        elements.append(
            Paragraph(
                (
                    f'FoodGram| Список покупок, от: '
                    f'{dt.datetime.now().strftime("%d.%m.%Yг.")} |FoodGram'
                ),
                self.RIGHT_HEADER_STYLE,
            ),
        )
        elements.append(flowables.HRFlowable(width='100%', spaceAfter=10))

        ingredients = dict()
        recipes = []
        shopping_cart = (
            self.current_user.shopping_list.all()
            .select_related('recipe', 'recipe__author')
            .order_by('recipe__name')
        )

        for shopping_element in shopping_cart:
            recipes.append(
                (
                    f'{shopping_element.recipe.name}, '
                    f'автор: {shopping_element.recipe.author}'
                )
            )
            for recipe_ingredient in (
                shopping_element.recipe.recipe_ingredients.all()
                .select_related('ingredient', 'recipe')
                .order_by('ingredient__name')
            ):
                if not recipe_ingredient.ingredient in ingredients:
                    ingredients[recipe_ingredient.ingredient] = 0

                ingredients[recipe_ingredient.ingredient] += (
                    recipe_ingredient.amount or 0
                )

        elements.append(
            Paragraph(
                f'Рецепты: ',
                self.BOLD_STYLE,
            )
        )

        for recipe in recipes:
            elements.append(
                Paragraph(
                    f'<bullet>&bull;</bullet>{recipe};',
                    self.LIST_STYLE,
                )
            )
        elements.append(Spacer(doc.width, 5))

        elements.append(
            Paragraph(
                f'Список покупок:',
                self.BOLD_STYLE,
            )
        )

        ingredients_table_data = []
        for ingredient, amount in ingredients.items():
            ingredients_table_data.append(
                [
                    Paragraph(f'{ingredient}', self.NORMAL_STYLE),
                    Paragraph(
                        f'{amount} {ingredient.measurement_unit}',
                        self.NORMAL_STYLE,
                    ),
                ],
            )

        if len(ingredients_table_data) == 0:
            ingredients_table_data = [
                [Paragraph(f'Список покупок пуст.', self.NORMAL_STYLE)],
            ]
        ingredients_table = Table(
            ingredients_table_data,
            hAlign='LEFT',
        )
        elements.append(ingredients_table)
        elements.append(Spacer(doc.width, 5))
        elements.append(flowables.HRFlowable(width='100%', spaceAfter=10))

        doc.build(elements)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf
