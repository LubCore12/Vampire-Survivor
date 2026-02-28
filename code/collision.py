class Collision:
    @staticmethod
    def collision(move_direction, direction, hitbox_rect, collision_sprites):
        for sprite in collision_sprites:
            if sprite.rect.colliderect(hitbox_rect):
                if move_direction == 'horizontal':
                    if direction.x > 0:
                        hitbox_rect.right = sprite.rect.left
                    if direction.x < 0:
                        hitbox_rect.left = sprite.rect.right
                if move_direction == 'vertical':
                    if direction.y > 0:
                        hitbox_rect.bottom = sprite.rect.top
                    if direction.y < 0:
                        hitbox_rect.top = sprite.rect.bottom