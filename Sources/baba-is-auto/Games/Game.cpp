#include <baba-is-auto/Games/Game.hpp>

namespace baba_is_auto
{
Game::Game(std::string_view filename)
{
    m_map.Load(filename);
}

void Game::Initialize()
{
    const std::size_t width = m_map.GetWidth();
    const std::size_t height = m_map.GetHeight();

    for (std::size_t y = 0; y < height; ++y)
    {
        for (std::size_t x = 0; x < width; ++x)
        {
            ParseRule(y, x, RuleDirection::HORIZONTAL);
            ParseRule(y, x, RuleDirection::VERTICAL);
        }
    }

    m_playerIcon = m_ruleManager.FindPlayer();
}

Map& Game::GetMap()
{
    return m_map;
}

RuleManager& Game::GetRuleManager()
{
    return m_ruleManager;
}

ObjectType Game::GetPlayerIcon() const
{
    return m_playerIcon;
}

void Game::ParseRule(std::size_t row, std::size_t col, RuleDirection direction)
{
    const std::size_t width = m_map.GetWidth();
    const std::size_t height = m_map.GetHeight();

    if (direction == RuleDirection::HORIZONTAL)
    {
        if (col + 2 >= width)
        {
            return;
        }

        if (IsNounType(m_map.At(row, col).GetType()) &&
            IsVerbType(m_map.At(row, col + 1).GetType()) &&
            (IsNounType(m_map.At(row, col + 2).GetType()) ||
             IsPropertyType(m_map.At(row, col + 2).GetType())))
        {
            m_ruleManager.Add({ m_map.At(row, col), m_map.At(row, col + 1),
                                m_map.At(row, col + 2) });
        }
    }
    else if (direction == RuleDirection::VERTICAL)
    {
        if (row + 2 >= height)
        {
            return;
        }

        if (IsNounType(m_map.At(row, col).GetType()) &&
            IsVerbType(m_map.At(row + 1, col).GetType()) &&
            (IsNounType(m_map.At(row + 2, col).GetType()) ||
             IsPropertyType(m_map.At(row + 2, col).GetType())))
        {
            m_ruleManager.Add({ m_map.At(row, col), m_map.At(row + 1, col),
                                m_map.At(row + 2, col) });
        }
    }
}

bool Game::CanMove(std::size_t _row, std::size_t _col, Direction dir)
{
    int row = static_cast<int>(_row);
    int col = static_cast<int>(_col);

    const auto width = static_cast<int>(m_map.GetWidth());
    const auto height = static_cast<int>(m_map.GetHeight());

    int dRow = 0, dCol = 0;
    if (dir == Direction::UP)
    {
        dRow = -1;
    }
    else if (dir == Direction::DOWN)
    {
        dRow = 1;
    }
    else if (dir == Direction::LEFT)
    {
        dCol = -1;
    }
    else if (dir == Direction::RIGHT)
    {
        dCol = 1;
    }

    row += dRow;
    col += dCol;

    // Check boundary
    if (row < 0 || row >= height || col < 0 || col >= width)
    {
        return false;
    }

    const ObjectType obj = m_map.At(row, col).GetType();

    // Check the icon has property 'STOP'.
    if (m_ruleManager.HasProperty(obj, ObjectType::STOP))
    {
        return false;
    }

    if (m_ruleManager.HasProperty(obj, ObjectType::PUSH))
    {
        if (!CanMove(row, col, dir))
        {
            return false;
        }
    }

    return true;
}

void Game::ProcessMove(std::size_t _row, std::size_t _col, Direction dir)
{
    int row = static_cast<int>(_row);
    int col = static_cast<int>(_col);

    int dRow = 0, dCol = 0;
    if (dir == Direction::UP)
    {
        dRow = -1;
    }
    else if (dir == Direction::DOWN)
    {
        dRow = 1;
    }
    else if (dir == Direction::LEFT)
    {
        dCol = -1;
    }
    else if (dir == Direction::RIGHT)
    {
        dCol = 1;
    }

    row += dRow;
    col += dCol;

    const ObjectType obj = m_map.At(row, col).GetType();

    if (m_ruleManager.HasProperty(obj, ObjectType::PUSH))
    {
        ProcessMove(row, col, dir);
    }

    m_map.Assign(row, col, m_map.At(_row, _col).GetType());
    m_map.Assign(_row, _col, ObjectType::ICON_EMPTY);
}
}  // namespace baba_is_auto