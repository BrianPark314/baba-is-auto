#ifndef BABA_IS_AUTO_NOUN_HPP
#define BABA_IS_AUTO_NOUN_HPP

#include <baba-is-auto/Enums/GameEnums.hpp>

#include <vector>

namespace baba_is_auto
{
//!
//! \brief Noun class.
//!
//! This class represents object such as noun, operator and property.
//! A noun is a word that corresponds to any possible in-game sprite. A few
//! nouns like STAR) have multiple corresponding sprites, while VIOLET and
//! FLOWER words have the same corresponding sprites. A noun can be used as a
//! NOUN IS VERB statement e.g. BABA IS YOU to give it a property or as a NOUN
//! IS NOUN statement e.g. WALL IS WATER to turn an object into another object.
//! An operator is a word that goes in between properties and nouns to show the
//! relation between them.
//! A property is something that can be attached to noun words to alter their
//! behavior.
//!
class Object
{
 public:
    //! Default constructor.
    Object() = default;

    //! Constructs an object.
    //! \param types A list of object types.
    explicit Object(std::vector<ObjectType> types);

    //! Operator overloading for ==.
    //! \param rhs A right side of Object object.
    //! \return The value that indicates two objects are equal.
    bool operator==(const Object& rhs) const;

    //! Gets a list of object types.
    //! \return A list of object types.
    std::vector<ObjectType> GetTypes() const;

 private:
    std::vector<ObjectType> m_types;
};
}  // namespace baba_is_auto

#endif