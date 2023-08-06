#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float32.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/float32.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/builtins/zip.hpp>
#include <pythonic/include/numpy/log.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/numpy/where.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/lt.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/builtins/zip.hpp>
#include <pythonic/numpy/log.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/numpy/where.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/lt.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_subpix
{
  struct __transonic__
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef pythonic::types::str __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  ;
    inline
    typename type::result_type operator()() const;
    ;
  }  ;
  struct compute_subpix_2d_gaussian2
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef long __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::log{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef pythonic::types::contiguous_slice __type3;
      typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type3>(), std::declval<__type3>()))>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::zip{})>::type>::type __type5;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::where{})>::type>::type __type6;
      typedef decltype(pythonic::operator_::lt(std::declval<__type4>(), std::declval<__type0>())) __type8;
      typedef decltype(std::declval<__type6>()(std::declval<__type8>())) __type9;
      typedef typename pythonic::lazy<__type9>::type __type10;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type10>::type>::type __type11;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type10>::type>::type __type13;
      typedef decltype(std::declval<__type5>()(std::declval<__type11>(), std::declval<__type13>())) __type14;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type15>::type>::type __type16;
      typedef typename pythonic::lazy<__type16>::type __type17;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type15>::type>::type __type19;
      typedef typename pythonic::lazy<__type19>::type __type20;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type17>(), std::declval<__type20>())) __type21;
      typedef indexable<__type21> __type22;
      typedef typename __combined<__type4,__type22>::type __type23;
      typedef double __type24;
      typedef container<typename std::remove_reference<__type24>::type> __type25;
      typedef typename __combined<__type23,__type25,__type22,__type25>::type __type26;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type0>(), std::declval<__type0>())) __type27;
      typedef decltype(std::declval<__type26>()[std::declval<__type27>()]) __type28;
      typedef decltype(std::declval<__type1>()(std::declval<__type28>())) __type29;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type29>())) __type30;
      typedef decltype(pythonic::operator_::div(std::declval<__type30>(), std::declval<__type0>())) __type31;
      typedef typename pythonic::assignable<long>::type __type32;
      typedef decltype(pythonic::operator_::add(std::declval<__type32>(), std::declval<__type30>())) __type37;
      typedef typename __combined<__type32,__type37>::type __type38;
      typedef decltype(pythonic::operator_::add(std::declval<__type38>(), std::declval<__type30>())) __type43;
      typedef typename __combined<__type38,__type43>::type __type44;
      typedef decltype(pythonic::operator_::add(std::declval<__type44>(), std::declval<__type30>())) __type49;
      typedef typename __combined<__type44,__type49>::type __type50;
      typedef decltype(pythonic::operator_::add(std::declval<__type50>(), std::declval<__type30>())) __type55;
      typedef typename __combined<__type50,__type55>::type __type56;
      typedef decltype(pythonic::operator_::add(std::declval<__type56>(), std::declval<__type30>())) __type61;
      typedef typename __combined<__type56,__type61>::type __type62;
      typedef decltype(pythonic::operator_::add(std::declval<__type62>(), std::declval<__type30>())) __type67;
      typedef typename __combined<__type62,__type67>::type __type68;
      typedef decltype(pythonic::operator_::add(std::declval<__type68>(), std::declval<__type30>())) __type73;
      typedef typename __combined<__type68,__type73>::type __type74;
      typedef decltype(pythonic::operator_::add(std::declval<__type74>(), std::declval<__type30>())) __type79;
      typedef typename __combined<__type74,__type79>::type __type80;
      typedef decltype(pythonic::operator_::add(std::declval<__type80>(), std::declval<__type30>())) __type85;
      typedef typename __combined<__type80,__type85>::type __type86;
      typedef typename __combined<__type86,__type30,__type30,__type30,__type30,__type30,__type30,__type30,__type30,__type30>::type __type87;
      typedef decltype(pythonic::operator_::div(std::declval<__type87>(), std::declval<__type0>())) __type88;
      typedef typename pythonic::assignable<decltype(pythonic::types::make_tuple(std::declval<__type31>(), std::declval<__type88>(), std::declval<__type88>(), std::declval<__type88>(), std::declval<__type88>(), std::declval<__type88>()))>::type __type313;
      typedef std::integral_constant<long,1> __type314;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type313>::type>::type __type316;
      typedef indexable_container<__type314, typename std::remove_reference<__type316>::type> __type317;
      typedef std::integral_constant<long,2> __type318;
      typedef typename __combined<__type313,__type317>::type __type319;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type319>::type>::type __type320;
      typedef indexable_container<__type318, typename std::remove_reference<__type320>::type> __type321;
      typedef typename __combined<__type313,__type317,__type321>::type __type322;
      typedef typename pythonic::assignable<typename std::tuple_element<3,typename std::remove_reference<__type322>::type>::type>::type __type323;
      typedef typename pythonic::assignable<typename std::tuple_element<2,typename std::remove_reference<__type319>::type>::type>::type __type324;
      typedef decltype(pythonic::operator_::mul(std::declval<__type323>(), std::declval<__type324>())) __type325;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type313>::type>::type>::type __type326;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type326>())) __type327;
      typedef std::integral_constant<long,3> __type328;
      typedef typename std::tuple_element<3,typename std::remove_reference<__type322>::type>::type __type329;
      typedef indexable_container<__type328, typename std::remove_reference<__type329>::type> __type330;
      typedef std::integral_constant<long,4> __type331;
      typedef typename __combined<__type313,__type317,__type321,__type330>::type __type332;
      typedef typename std::tuple_element<4,typename std::remove_reference<__type332>::type>::type __type333;
      typedef indexable_container<__type331, typename std::remove_reference<__type333>::type> __type334;
      typedef typename __combined<__type313,__type317,__type321,__type330,__type334>::type __type335;
      typedef typename pythonic::assignable<typename std::tuple_element<5,typename std::remove_reference<__type335>::type>::type>::type __type336;
      typedef decltype(pythonic::operator_::mul(std::declval<__type327>(), std::declval<__type336>())) __type337;
      typedef decltype(pythonic::operator_::sub(std::declval<__type325>(), std::declval<__type337>())) __type338;
      typedef typename pythonic::assignable<typename std::tuple_element<4,typename std::remove_reference<__type332>::type>::type>::type __type339;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type339>())) __type340;
      typedef decltype(pythonic::operator_::mul(std::declval<__type340>(), std::declval<__type336>())) __type342;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type __type343;
      typedef decltype(std::declval<__type343>()(std::declval<__type323>())) __type345;
      typedef decltype(pythonic::operator_::sub(std::declval<__type342>(), std::declval<__type345>())) __type346;
      typedef decltype(pythonic::operator_::div(std::declval<__type338>(), std::declval<__type346>())) __type347;
      typedef decltype(pythonic::operator_::mul(std::declval<__type323>(), std::declval<__type326>())) __type350;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type324>())) __type352;
      typedef decltype(pythonic::operator_::mul(std::declval<__type352>(), std::declval<__type339>())) __type354;
      typedef decltype(pythonic::operator_::sub(std::declval<__type350>(), std::declval<__type354>())) __type355;
      typedef decltype(pythonic::operator_::div(std::declval<__type355>(), std::declval<__type346>())) __type363;
      typedef typename __combined<__type23,__type25,__type22>::type __type364;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type347>(), std::declval<__type363>(), std::declval<__type364>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    inline
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& correl, argument_type1&& ix, argument_type2&& iy) const
    ;
  }  ;
  inline
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.11"));
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  inline
  typename compute_subpix_2d_gaussian2::type<argument_type0, argument_type1, argument_type2>::result_type compute_subpix_2d_gaussian2::operator()(argument_type0&& correl, argument_type1&& ix, argument_type2&& iy) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
    typedef pythonic::types::contiguous_slice __type1;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type1>()))>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::zip{})>::type>::type __type3;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::where{})>::type>::type __type4;
    typedef long __type6;
    typedef decltype(pythonic::operator_::lt(std::declval<__type2>(), std::declval<__type6>())) __type7;
    typedef decltype(std::declval<__type4>()(std::declval<__type7>())) __type8;
    typedef typename pythonic::lazy<__type8>::type __type9;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type9>::type>::type __type10;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type9>::type>::type __type12;
    typedef decltype(std::declval<__type3>()(std::declval<__type10>(), std::declval<__type12>())) __type13;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type13>::type::iterator>::value_type>::type __type14;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type14>::type>::type __type15;
    typedef typename pythonic::lazy<__type15>::type __type16;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type14>::type>::type __type18;
    typedef typename pythonic::lazy<__type18>::type __type19;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type16>(), std::declval<__type19>())) __type20;
    typedef indexable<__type20> __type21;
    typedef typename __combined<__type2,__type21>::type __type22;
    typedef double __type23;
    typedef container<typename std::remove_reference<__type23>::type> __type24;
    typedef typename pythonic::assignable<long>::type __type25;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::log{})>::type>::type __type26;
    typedef typename __combined<__type22,__type24,__type21>::type __type27;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type6>(), std::declval<__type6>())) __type28;
    typedef decltype(std::declval<__type27>()[std::declval<__type28>()]) __type29;
    typedef decltype(std::declval<__type26>()(std::declval<__type29>())) __type30;
    typedef decltype(pythonic::operator_::mul(std::declval<__type6>(), std::declval<__type30>())) __type31;
    typedef decltype(pythonic::operator_::add(std::declval<__type25>(), std::declval<__type31>())) __type32;
    typedef typename __combined<__type25,__type32>::type __type33;
    typedef decltype(pythonic::operator_::add(std::declval<__type33>(), std::declval<__type31>())) __type38;
    typedef typename __combined<__type33,__type38>::type __type39;
    typedef decltype(pythonic::operator_::add(std::declval<__type39>(), std::declval<__type31>())) __type44;
    typedef typename __combined<__type39,__type44>::type __type45;
    typedef decltype(pythonic::operator_::add(std::declval<__type45>(), std::declval<__type31>())) __type50;
    typedef typename __combined<__type45,__type50>::type __type51;
    typedef decltype(pythonic::operator_::add(std::declval<__type51>(), std::declval<__type31>())) __type56;
    typedef typename __combined<__type51,__type56>::type __type57;
    typedef decltype(pythonic::operator_::add(std::declval<__type57>(), std::declval<__type31>())) __type62;
    typedef typename __combined<__type57,__type62>::type __type63;
    typedef decltype(pythonic::operator_::add(std::declval<__type63>(), std::declval<__type31>())) __type68;
    typedef typename __combined<__type63,__type68>::type __type69;
    typedef decltype(pythonic::operator_::add(std::declval<__type69>(), std::declval<__type31>())) __type74;
    typedef typename __combined<__type69,__type74>::type __type75;
    typedef decltype(pythonic::operator_::add(std::declval<__type75>(), std::declval<__type31>())) __type80;
    typedef typename __combined<__type75,__type80>::type __type81;
    typedef decltype(pythonic::operator_::div(std::declval<__type31>(), std::declval<__type6>())) __type302;
    typedef typename __combined<__type81,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31>::type __type303;
    typedef decltype(pythonic::operator_::div(std::declval<__type303>(), std::declval<__type6>())) __type304;
    typedef typename pythonic::assignable<decltype(pythonic::types::make_tuple(std::declval<__type302>(), std::declval<__type304>(), std::declval<__type304>(), std::declval<__type304>(), std::declval<__type304>(), std::declval<__type304>()))>::type __type313;
    typedef std::integral_constant<long,1> __type314;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type313>::type>::type __type316;
    typedef indexable_container<__type314, typename std::remove_reference<__type316>::type> __type317;
    typedef std::integral_constant<long,2> __type318;
    typedef typename __combined<__type313,__type317>::type __type319;
    typedef typename std::tuple_element<2,typename std::remove_reference<__type319>::type>::type __type320;
    typedef indexable_container<__type318, typename std::remove_reference<__type320>::type> __type321;
    typedef std::integral_constant<long,3> __type322;
    typedef typename __combined<__type313,__type317,__type321>::type __type323;
    typedef typename std::tuple_element<3,typename std::remove_reference<__type323>::type>::type __type324;
    typedef indexable_container<__type322, typename std::remove_reference<__type324>::type> __type325;
    typedef std::integral_constant<long,4> __type326;
    typedef typename __combined<__type313,__type317,__type321,__type325>::type __type327;
    typedef typename std::tuple_element<4,typename std::remove_reference<__type327>::type>::type __type328;
    typedef indexable_container<__type326, typename std::remove_reference<__type328>::type> __type329;
    typedef std::integral_constant<long,5> __type330;
    typedef typename __combined<__type313,__type317,__type321,__type325,__type329>::type __type331;
    typedef typename std::tuple_element<5,typename std::remove_reference<__type331>::type>::type __type332;
    typedef indexable_container<__type330, typename std::remove_reference<__type332>::type> __type333;
    typename pythonic::assignable<typename __combined<__type22,__type24,__type21>::type>::type correl_crop = correl(pythonic::types::contiguous_slice(pythonic::operator_::sub(iy, 1L),pythonic::operator_::add(iy, 2L)),pythonic::types::contiguous_slice(pythonic::operator_::sub(ix, 1L),pythonic::operator_::add(ix, 2L)));
    typename pythonic::lazy<decltype(pythonic::numpy::functor::where{}(pythonic::operator_::lt(correl_crop, 0L)))>::type tmp = pythonic::numpy::functor::where{}(pythonic::operator_::lt(correl_crop, 0L));
    {
      for (auto&& __tuple0: pythonic::builtins::functor::zip{}(std::get<0>(tmp), std::get<1>(tmp)))
      {
        typename pythonic::lazy<decltype(std::get<1>(__tuple0))>::type i1 = std::get<1>(__tuple0);
        typename pythonic::lazy<decltype(std::get<0>(__tuple0))>::type i0 = std::get<0>(__tuple0);
        correl_crop[pythonic::types::make_tuple(i0, i1)] = 1e-06;
      }
    }
    typename pythonic::assignable<typename __combined<__type81,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31>::type>::type c10 = 0L;
    typename pythonic::assignable<typename __combined<__type81,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31>::type>::type c01 = 0L;
    typename pythonic::assignable<typename __combined<__type81,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31>::type>::type c11 = 0L;
    typename pythonic::assignable<typename __combined<__type81,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31>::type>::type c20 = 0L;
    typename pythonic::assignable<typename __combined<__type81,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31,__type31>::type>::type c02 = 0L;
    c10 += pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 0L))));
    c01 += pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 0L))));
    c11 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 0L))));
    c20 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 0L))));
    c02 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 0L))));
    c10 += pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 0L))));
    c01 += pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 0L))));
    c11 += pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 0L))));
    c20 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 0L))));
    c02 += pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 0L))));
    c10 += pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 0L))));
    c01 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 0L))));
    c11 += pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 0L))));
    c20 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 0L))));
    c02 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 0L))));
    c10 += pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 1L))));
    c01 += pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 1L))));
    c11 += pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 1L))));
    c20 += pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 1L))));
    c02 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 1L))));
    c10 += pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 1L))));
    c01 += pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 1L))));
    c11 += pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 1L))));
    c20 += pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 1L))));
    c02 += pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 1L))));
    c10 += pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 1L))));
    c01 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 1L))));
    c11 += pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 1L))));
    c20 += pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 1L))));
    c02 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 1L))));
    c10 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 2L))));
    c01 += pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 2L))));
    c11 += pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 2L))));
    c20 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 2L))));
    c02 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(0L, 2L))));
    c10 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 2L))));
    c01 += pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 2L))));
    c11 += pythonic::operator_::mul(0L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 2L))));
    c20 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 2L))));
    c02 += pythonic::operator_::mul(-2L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(1L, 2L))));
    c10 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L))));
    c01 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L))));
    c11 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L))));
    c20 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L))));
    c02 += pythonic::operator_::mul(1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L))));
    typename pythonic::assignable<typename __combined<__type313,__type317,__type321,__type325,__type329,__type333>::type>::type __tuple1 = pythonic::types::make_tuple(pythonic::operator_::div(pythonic::operator_::mul(-1L, pythonic::numpy::functor::log{}(correl_crop.fast(pythonic::types::make_tuple(2L, 2L)))), 9L), pythonic::operator_::div(c10, 6L), pythonic::operator_::div(c01, 6L), pythonic::operator_::div(c11, 4L), pythonic::operator_::div(c20, 6L), pythonic::operator_::div(c02, 6L));
    typename pythonic::assignable_noescape<decltype(std::get<1>(__tuple1))>::type c10_ = std::get<1>(__tuple1);
    typename pythonic::assignable_noescape<decltype(std::get<2>(__tuple1))>::type c01_ = std::get<2>(__tuple1);
    typename pythonic::assignable_noescape<decltype(std::get<3>(__tuple1))>::type c11_ = std::get<3>(__tuple1);
    typename pythonic::assignable_noescape<decltype(std::get<4>(__tuple1))>::type c20_ = std::get<4>(__tuple1);
    typename pythonic::assignable_noescape<decltype(std::get<5>(__tuple1))>::type c02_ = std::get<5>(__tuple1);
    return pythonic::types::make_tuple(pythonic::operator_::div(pythonic::operator_::sub(pythonic::operator_::mul(c11_, c01_), pythonic::operator_::mul(pythonic::operator_::mul(2L, c10_), c02_)), pythonic::operator_::sub(pythonic::operator_::mul(pythonic::operator_::mul(4L, c20_), c02_), pythonic::numpy::functor::square{}(c11_))), pythonic::operator_::div(pythonic::operator_::sub(pythonic::operator_::mul(c11_, c10_), pythonic::operator_::mul(pythonic::operator_::mul(2L, c01_), c20_)), pythonic::operator_::sub(pythonic::operator_::mul(pythonic::operator_::mul(4L, c20_), c02_), pythonic::numpy::functor::square{}(c11_))), correl_crop);
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_subpix::__transonic__()());
inline
typename __pythran_subpix::compute_subpix_2d_gaussian2::type<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>, long, long>::result_type compute_subpix_2d_gaussian20(pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>&& correl, long&& ix, long&& iy) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_subpix::compute_subpix_2d_gaussian2()(correl, ix, iy);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
inline
typename __pythran_subpix::compute_subpix_2d_gaussian2::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>, long, long>::result_type compute_subpix_2d_gaussian21(pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>&& correl, long&& ix, long&& iy) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_subpix::compute_subpix_2d_gaussian2()(correl, ix, iy);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_compute_subpix_2d_gaussian20(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"correl", "ix", "iy",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(compute_subpix_2d_gaussian20(from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_subpix_2d_gaussian21(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    
    char const* keywords[] = {"correl", "ix", "iy",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]) && is_convertible<long>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(compute_subpix_2d_gaussian21(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,pythonic::types::pshape<long,long>>>>(args_obj[0]), from_python<long>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_subpix_2d_gaussian2(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_subpix_2d_gaussian20(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_subpix_2d_gaussian21(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_subpix_2d_gaussian2", "\n""    - compute_subpix_2d_gaussian2(float32[:,:], int, int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_subpix_2d_gaussian2",
    (PyCFunction)__pythran_wrapall_compute_subpix_2d_gaussian2,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n""\n""    - compute_subpix_2d_gaussian2(float32[:,:], int, int)"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "subpix",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(subpix)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
#if defined(GNUC) && !defined(__clang__)
__attribute__ ((externally_visible))
#endif
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(subpix)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("subpix",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.10.0",
                                      "2021-09-30 15:37:35.257457",
                                      "8212ffb238fa5b6ba52c971aee55b9efeed33b97b93b1c8d70f090f83d6e39a3");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PyModule_AddObject(theModule, "__transonic__", __transonic__);
    PYTHRAN_RETURN;
}

#endif