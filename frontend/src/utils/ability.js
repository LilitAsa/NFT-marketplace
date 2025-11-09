export const can = (user, required) => !required.length || required.includes(user?.role);

// скрытие элементов UI по роли
// использование:
// {can(user, ['pro', 'admin']) && <Button onClick={openProTooling}>Pro tools</Button>}