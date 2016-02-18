/*!
    @file MapArray.tpp
    @brief Typemap class MapArray
    @author CIMON Lucas
    @date november 2011
*/
#ifndef _DEF_H_MapArray
#define _DEF_H_MapArray

#include <map>
#include <vector>

/*
    Fixed size vectors with log(n) reverse-access
    
    WHY FIXED SIZE ?
    => if vector reallocated => pointers invalided => reverse-search map invalided

    TODO-WARNING: test it again, segfaults seem to occurs in R&B tree

    You'll probably need to define :

    namespace std {
        template <>
        class less<const T*> {
        public:
            bool operator()(const T*, const T*) const;
        };
    }
*/

    template<typename T>
    class MapArray {
    private:
        std::vector<T> owner_;
        std::map<const T*, size_t> indices_;
    
    public:
        MapArray(size_t fixedSize) : owner_(), indices_() {
            owner_.reserve(fixedSize);
        }
        MapArray(const MapArray& mA) : owner_(mA.owner_), indices_() {
            const size_t nbElem = mA.indices_.size();
            for (size_t i = 0; i < nbElem; ++i)
                indices_[&owner_[i]] = i;
        }
        size_t size() const {
            return owner_.size();
        }
        // Cost = 2*log(size)
        int insert(const T& v) {
            int index = find(v);
            if (index != -1)
                return index;
            index = static_cast<int>(owner_.size());
            owner_.push_back(v);
            indices_[&owner_[index]] = index;
            return index;
        }
        // Cost = log(size)
        int find(const T& v) const {
            typename std::map<const T*, size_t>::const_iterator it = indices_.find(&v);
            if (it != indices_.end())
                return static_cast<int>(it->second);
            return -1;
        }
        T& operator[](size_t i) {
            return owner_[i];
        }
        const T& operator[](size_t i) const {
            return owner_[i];
        }
        void clear() {
            owner_.clear();
            indices_.clear();
        }
        std::vector<T>& array() { return owner_; };
        const std::vector<T>& array() const { return owner_; };
    };

/*
    Slow, safe methods without map :

        // Cost = cost(find)
        int insert(const T& v) {
            int index = find(v);
            if (index != -1)
                return index;
            index = static_cast<int>(owner_.size());
            owner_.push_back(v);
            return index;
        }
    
        // Cost = O(size)
        int find(const T& v) const {
            std::less<const T*> functor;
            for (unsigned int i = 0; i < owner_.size(); ++i)
                if (!functor(&v, &owner_[i]) && !functor(&owner_[i], &v))
                    return i;
            return -1;
        }    
    */

#endif // _DEF_H_MapArray
