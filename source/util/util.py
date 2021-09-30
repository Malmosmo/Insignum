import pygame


def renderImage(screen, img, x, y, center=False):
    if center:
        rect = img.get_rect(center=(x, y))

    else:
        rect = img.get_rect()

    screen.blit(img, rect)


def renderText(screen, text, color, x, y, font, center=False):
    img = font.render(text, True, color)

    if center:
        rect = img.get_rect(center=(x, y))

    else:
        rect = img.get_rect()

    screen.blit(img, rect)


def loadImage(path):
    image = pygame.image.load(path)
    image = image.convert_alpha()

    return image


def scale(img, scale):
    return pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
